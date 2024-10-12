"""
Main user function to retrieve snow depth with snow depth and wet snow flag
"""
import os
from os.path import join
from pathlib import Path
import glob
import json
import pandas as pd
import xarray as xr
import shapely.geometry
from typing import Tuple, Union, List
import logging
import shapely
import os
from typing import Optional
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
# Add main repo to path
import sys
from os.path import expanduser

from asf_snow.utils.utils import read_environment, write_environment
from asf_snow.utils import utils
# Add main repo to path if you haven't added with conda-develop
# import sys
# sys.path.append('path/to/the/spicy-snow/')

# from spicy_snow.retrieval import retrieve_snow_depth
# from asf_snow.retrieval_snow_depth_sentinel_1c import retrieve_snow_depth

from spicy_snow.IO.user_dates import get_input_dates


process_status = {"begin": 0, "check": 1, "sentinel1": 2, "snow": 3, "fcf": 4,
                  "preprocess": 5, "calculate": 6, "output": 7}

sys.path.append(expanduser('../'))

# import functions for downloading
# from asf_snow.utils.utils import read_environment, write_environment
from asf_snow.download.sentinel1 import s1_img_search, hyp3_pipeline, download_hyp3, combine_s1_images, files2dataarray
#from spicy_snow.download.forest_cover import download_fcf
from asf_snow.download.forest_cover import download_fcf
from asf_snow.download.snow_cover import download_snow_cover

# import functions for pre-processing
from spicy_snow.processing.s1_preprocessing import merge_partial_s1_images, s1_orbit_averaging, \
    s1_clip_outliers, subset_s1_images, ims_water_mask, s1_incidence_angle_masking, merge_s1_subsets, \
    add_confidence_angle

# import the functions for snow_index calculation
from asf_snow.processing.snow_index import calc_delta_VV, calc_delta_cross_ratio, \
    calc_delta_gamma, clip_delta_gamma_outlier, calc_snow_index, calc_snow_index_to_snow_depth


# import the functions for wet snow flag
from spicy_snow.processing.wet_snow import id_newly_frozen_snow, id_newly_wet_snow, \
    id_wet_negative_si, flag_wet_snow

# setup root logger
from spicy_snow.utils.spicy_logging import setup_logging

log = logging.getLogger(__name__)


def download_sentinel1_data(area: shapely.geometry.Polygon, dates: Tuple[str, str], work_dir: str = './',
                   job_name: str = 'spicy-snow-run', existing_job_name: Union[bool, str] = False, environment=None):

    outdir = join(work_dir, 'tmp')
    log = logging.getLogger(__name__)

    # get asf_search search results
    search_results = s1_img_search(area, dates)
    log.info(f'Found {len(search_results)} results')

    num = len(search_results)

    if len(glob.glob(f'{outdir}/*.zip')) == num or len(glob.glob(f'{outdir}/S1*_VV.tif')) == num:
        if len(glob.glob(f'{outdir}/S1*_VV.tif')) == num:
            filelist = glob.glob(f'{outdir}/S1*_VV.tif')
        else:
            filelist = glob.glob(f'{outdir}/*.zip')
        imgs = files2dataarray(filelist, area=area, outdir=outdir, clean=False)
    else:

        assert len(search_results) > 3, f"Need at least 4 images to run. Found {len(search_results)} \
            using area: {area} and dates: {dates}."

        # download s1 images into dataset ['s1'] variable name
        jobs = hyp3_pipeline(search_results, job_name=job_name, existing_job_name=existing_job_name)
        imgs = download_hyp3(jobs, area, outdir=join(work_dir, 'tmp'), clean=False)

    # img is a dictionary where each value is a xarray.DataArray.
    ds = combine_s1_images(imgs)

    # merge partial images together
    ds = merge_partial_s1_images(ds)

    ds.to_netcdf(f'{outdir}/sentinel1.nc')

    environment['step'] = 'sentinel1'
    os.environ['ENVIRONMENT'] = json.dumps(environment)
    write_environment(environment, f'{work_dir}/tmp/environment.json')

    return ds


def preprocess(ds, environment):
    log = logging.getLogger(__name__)
    log.info("Preprocessing Sentinel-1 images")

    # step: preprocessing
    # TODO add water mask
    # ds = ims_water_mask(ds)

    # mask out outliers in incidence angle
    ds = s1_incidence_angle_masking(ds)

    # subset dataset by flight_dir and platform
    dict_ds = subset_s1_images(ds)

    for subset_name, subset_ds in dict_ds.items():
        # average each orbit to overall mean
        dict_ds[subset_name] = s1_orbit_averaging(subset_ds)
        # clip outlier values of backscatter to overall mean
        dict_ds[subset_name] = s1_clip_outliers(subset_ds)

    # recombine subsets
    ds = merge_s1_subsets(dict_ds)

    # calculate confidence interval
    ds = add_confidence_angle(ds)
    ds.to_netcdf(f'{environment['workdir']}/tmp/processed_ds.nc')

    # update environment
    environment['step'] = 'preprocess'
    os.environ['ENVIRONMENT'] = json.dumps(environment)
    write_environment(environment, f'{environment['workdir']}/tmp/environment.json')

    return ds


def retrieve_snow_depth(area: shapely.geometry.Polygon,
                        dates: Tuple[str, str],
                        work_dir: str = './',
                        job_name: str = 'spicy-snow-run',
                        existing_job_name: Union[bool, str] = False,
                        debug: bool = False,
                        ims_masking: bool = True,
                        wet_snow_thresh: float = -2,
                        freezing_snow_thresh: float = 1,
                        wet_SI_thresh: float = 0,
                        outfp: Union[str, Path, bool] = False,
                        params: List[float] = [2.5, 0.2, 0.55]) -> xr.Dataset:
    """
    Finds, downloads Sentinel-1, forest cover, water mask (not implemented), and
    snow coverage. Then retrieves snow depth using Lievens et al. 2021 method.

    Args:
    area: Shapely geometry to use as bounding box of desired area to search within
    dates: Start and end date to search between
    work_dir: filepath to directory to work in. Will be created if not existing
    job_name: name for hyp3 job
    existing_job_name: name for preexisiting hyp3 job to download and avoid resubmitting
    debug: do you want to get verbose logging?
    ims_masking: do you want to mask pixels by IMS snow free imagery?
    wet_snow_thresh: what threshold in dB change to use for melting and re-freezing snow? Default: -2
    freezing_snow_thresh: what threshold in dB change to use for re-freezing snow id. Default: +2
    wet_SI_thresh: what threshold to use for negative snow index? Default: 0
    outfp: do you want to save netcdf? default is False and will just return dataset
    params: the A, B, C parameters to use in the model. Current defaults are optimized to north america

    Returns:
    datset: Xarray dataset with 'snow_depth' and 'wet_snow' variables for all Sentinel-1
    image acquistions in area and dates
    """
    # check the arguments
    log = logging.getLogger(__name__)
    log.info("Check the arguments...")

    assert isinstance(area, shapely.geometry.Polygon), f"Must provide shapely geometry for area. Got {type(area)}"

    assert isinstance(dates, list) or isinstance(dates, tuple)
    assert len(dates) == 2, f"Can only provide two dates to work between. Got {dates}"

    assert isinstance(work_dir, str) or isinstance(work_dir, Path)
    if isinstance(work_dir, Path):
        work_dir = str(work_dir)

    assert isinstance(debug, bool), f"Debug keyword must be boolean. Got {debug}"

    assert isinstance(params, list) or isinstance(params,
                                                  tuple), f"param keyword must be list or tuple. Got {type(params)}"
    assert len(params) == 3, f"List of params must be 3 in order A, B, C. Got {params}"
    A, B, C = params

    if type(outfp) != bool:
        outfp = Path(outfp).expanduser().resolve()
        assert outfp.parent.exists(), f"Out filepath {outfp}'s directory does not exist"

    os.makedirs(work_dir, exist_ok=True)
    setup_logging(log_dir=join(work_dir, 'logs'), debug=debug)

    if wet_snow_thresh >= 0:
        log.warning(
            f"Running with wet snow threshold of {wet_snow_thresh}. This value is positive but should be negative.")

    if freezing_snow_thresh <= 0:
        log.warning(
            f"Running with refreeze threshold of {freezing_snow_thresh}. This value is negative but should be positive.")

    # step: download_sentinel1_data
    log.info("Download sentinel1 data...")
    environment = json.loads(os.environ['ENVIRONMENT'])

    if process_status[environment['step']] < process_status["sentinel1"]:
        ds = download_sentinel1_data(area=area, dates=dates, work_dir=work_dir, job_name=job_name,
                                     existing_job_name=existing_job_name, environment=environment)
    elif process_status[environment['step']] == process_status["sentinel1"]:
        ds = xr.load_dataset(f'{work_dir}/tmp/sentinel1.nc')
    else:
        pass

    ''''
    # get asf_search search results
    search_results = s1_img_search(area, dates)
    log.info(f'Found {len(search_results)} results')

    assert len(search_results) > 3, f"Need at least 4 images to run. Found {len(search_results)} \
    using area: {area} and dates: {dates}."


    # download s1 images into dataset ['s1'] variable name
    jobs = hyp3_pipeline(search_results, job_name=job_name, existing_job_name=existing_job_name)
    imgs = download_hyp3(jobs, area, outdir=join(work_dir, 'tmp'), clean=False)
    ds = combine_s1_images(imgs)

    # merge partial images together
    ds = merge_partial_s1_images(ds)
    '''
    # step: download_snow_data, download IMS snow cover and add to dataset ['ims'] keyword
    log.info("Download snow data...")
    if process_status[environment['step']] < process_status["snow"]:
        ds = download_snow_cover(ds, tmp_dir=join(work_dir, 'tmp'), clean=False,)
        environment['step'] = 'snow'
        os.environ['ENVIRONMENT'] = json.dumps(environment)
        write_environment(environment, f'{work_dir}/tmp/environment.json')

    elif process_status[environment['step']] == process_status["snow"]:
        ds = xr.load_dataset(f'{work_dir}/tmp/sentinel1_snow.nc')
    else:
        pass

    # step: download_fcf_data, download fcf and add to dataset ['fcf'] keyword
    log.info("Download fcf data...")
    if process_status[environment['step']] < process_status["fcf"]:
        ds = download_fcf(ds, join(work_dir, 'tmp', 'fcf.tif'), environment=environment)
        environment['step'] = 'fcf'
        os.environ['ENVIRONMENT'] = json.dumps(environment)
        write_environment(environment, f'{work_dir}/tmp/environment.json')

    elif process_status[environment['step']] == process_status["fcf"]:
        ds = xr.load_dataset(f'{work_dir}/tmp/sentinel1_snow_fcf.nc')
    else:
        pass

    # Step: Preprocess
    log.info("Preprocess...")

    if process_status[environment['step']] < process_status["preprocess"]:
        ds = preprocess(ds, environment)

    elif process_status[environment['step']] == process_status["preprocess"]:
        ds = xr.load_dataset(f'{work_dir}/tmp/sentinel1_snow_fcf.nc')
    else:
        pass

    # Step: calculate
    log.info("Calculate snow depth...")
    '''
    if process_status[environment['step']] < process_status["calculate"]
        ds = xr.open_dataset(f'{work_dir}/tmp/calculate.nc')
    else:
    '''
    log.info("Calculating snow index")
    # calculate delta CR and delta VV
    ds = calc_delta_cross_ratio(ds, A=A)
    ds = calc_delta_VV(ds)

    # calculate delta gamma with delta CR and delta VV with FCF
    ds = calc_delta_gamma(ds, B=B)

    # clip outliers of delta gamma
    ds = clip_delta_gamma_outlier(ds)

    # calculate snow_index from delta_gamma
    ds = calc_snow_index(ds, ims_masking=ims_masking)

    # convert snow index to snow depth
    ds = calc_snow_index_to_snow_depth(ds, C=C)

    # wet Snow Flags
    log.info("Flag wet snow")
    # find newly wet snow
    ds = id_newly_wet_snow(ds, wet_thresh=wet_snow_thresh)
    ds = id_wet_negative_si(ds, wet_SI_thresh=wet_SI_thresh)

    # find newly frozen snow
    ds = id_newly_frozen_snow(ds, freeze_thresh=freezing_snow_thresh)

    # make wet_snow flag
    ds = flag_wet_snow(ds)

    ds.attrs['param_A'] = A
    ds.attrs['param_B'] = B
    ds.attrs['param_C'] = C

    ds.attrs['job_name'] = job_name

    ds.attrs['bounds'] = area.bounds

    # write the calculate.nc
    ds.to_netcdf(f'{work_dir}/tmp/calculate.nc')

    # update environment
    # environment['step'] = 'calculate'
    # os.environ['ENVIRONMENT'] = json.dumps(environment)
    # write_environment(environment, f'{environment['work_dir']}/tmp/environment.json')

    # Step: output
    log.info("Output snow depth product...")
    if outfp:
        outfp = str(outfp)

        ds.to_netcdf(outfp)

    log.info("Done...")
    return ds


def retrieval_from_parameters(dataset: xr.Dataset,
                              A: float,
                              B: float,
                              C: float,
                              wet_SI_thresh: float = 0,
                              freezing_snow_thresh: float = 2,
                              wet_snow_thresh: float = -2):
    """
    Retrieve snow depth with varied parameter set from an already pre-processed
    dataset.

    Args:
    dataset: Already preprocessed dataset with s1, fcf, ims, deltaVV, merged images,
    and masking applied.
    A: A parameter
    B: B parameter
    C: C parameter

    Returns:
    dataset: xarray dataset with snow_depth variable calculated from parameters
    """

    # dataset = dataset[['s1','deltaVV','ims','fcf','lidar-sd']]

    # load dataset to index
    dataset = dataset.load()

    # calculate delta CR and delta VV
    dataset = calc_delta_cross_ratio(dataset, A=A)

    # calculate delta gamma with delta CR and delta VV with FCF
    dataset = calc_delta_gamma(dataset, B=B)

    # clip outliers of delta gamma
    dataset = clip_delta_gamma_outlier(dataset)

    # calculate snow_index from delta_gamma
    dataset = calc_snow_index(dataset)

    # convert snow index to snow depth
    dataset = calc_snow_index_to_snow_depth(dataset, C=C)

    # find newly wet snow
    dataset = id_newly_wet_snow(dataset, wet_thresh=wet_snow_thresh)
    dataset = id_wet_negative_si(dataset, wet_SI_thresh=wet_SI_thresh)

    # find newly frozen snow
    dataset = id_newly_frozen_snow(dataset, freeze_thresh=freezing_snow_thresh)

    # make wet_snow flag
    dataset = flag_wet_snow(dataset)

    return dataset

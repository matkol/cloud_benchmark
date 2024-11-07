#!/usr/bin/env python

from google.cloud import storage
from functools import wraps
from timeit import default_timer
from flask import current_app
from celery.utils.log import get_task_logger


def timer(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start_time = default_timer()
        ret = f(*args, **kwargs)
        total_elapsed_time = default_timer() - start_time
        logger = current_app.logger if current_app else get_task_logger(__name__)
        logger.info('%s seconds for %s call!', total_elapsed_time, f.__name__)
        return ret

    return wrapper


@timer
def download_blob(bucket_name, source_blob_name, destination_file_name):

    storage_client = storage.Client(project='constellr-test')

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    logger = current_app.logger if current_app else get_task_logger(__name__)
    logger.info(
        "Downloaded storage object {} from bucket {} to local file {}.".format(
            source_blob_name, bucket_name, destination_file_name
        )
    )

#!/usr/bin/env python

import os
import time
from celery import Celery
from celery.utils.log import get_task_logger

from app.utils import download_blob


# Be careful with logger naming here
# See https://phdesign.com.au/programming/duplicate-celery-logs-in-flask/
logger = get_task_logger(__name__)

BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
BACKEND_URL = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")
celery = Celery('tasks', broker=BROKER_URL, backend=BACKEND_URL)


@celery.task(name='Add two numbers')
def add(x, y):
    logger.info('Adding {0} + {1}'.format(x, y))
    return x + y


@celery.task(bind=True)
def long_running_task(self, pause, **kwargs):
    logger.info("Got pause duration:%s", pause)
    logger.info("Got kwargs:%s", kwargs)
    time.sleep(pause)
    if kwargs:
        download_blob(kwargs['bucket'], kwargs['blob_name'], kwargs['local_name'])
    return f"Task completed after {pause} seconds."

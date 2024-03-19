from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.management import call_command
import random

import requests


logger = get_task_logger(__name__)


@shared_task
def sample_task():
    logger.info("The sample task just ran.")


@shared_task
def send_email_report():
    call_command("email_report", )
    
# @shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_jitter=True, retry_kwargs={'max_retries': 7, 'countdown': 3})
@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 7, 'countdown': 3})
def task_process_notification(self):
    if not random.choice([0,0,0,0,0,1]):
        logger.info("Errorrrrrrrrrrrrrrrr")
        # mimic random error
        raise Exception()

    logger.info("Non Errorrrrrrrrrrrrr")
    requests.post('https://httpbin.org/delay/5')
    
# class BaseTaskWithRetry(celery.Task):
#     autoretry_for = (Exception, KeyError)
#     retry_kwargs = {'max_retries': 5}
#     retry_backoff = True


# @shared_task(bind=True, base=BaseTaskWithRetry)
# def task_process_notification(self):
#     raise Exception()
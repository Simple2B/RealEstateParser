# flake8: noqa F501
import time
from celery import Celery
from config import BaseConfig as conf
from app.logger import log


log.set_level(log.DEBUG)
celery = Celery(__name__)
celery.conf.broker_url = conf.REDIS_URL
celery.conf.result_backend = conf.REDIS_URL


@celery.task
def scrape_sites(query):
    log(log.INFO, "Celery Scraping Task. Query: [%s]", query)
    # TODO subprocess run flask command

from celery import shared_task

from .services import save_log


@shared_task
def save_cache_log_task():
    save_log()

from celery import task
from datetime import timedelta


@task.periodic_task(run_every = timedelta(seconds=10),ignore_result=False)
def something():
    print("AYUSH KUMAr")
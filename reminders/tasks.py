from celery import task
from datetime import timedelta
import os
import pickle
from django.db import connection

from .utils import dictfetchall

@task.periodic_task(run_every = timedelta(seconds=10),ignore_result=False)
def something():
    with connection.cursor() as curr:
        curr.execute("SELECT user_id,description from reminders WHERE reminder_time <= CURRENT_TIMESTAMP")
        res = dictfetchall(curr)
        curr.execute("DELETE FROM reminders WHERE reminder_time <= CURRENT_TIMESTAMP")
    if os.path.isfile("reminders.pkl"):
        os.remove("reminders.pkl")
    file = open("reminders.pkl","wb")
    pickle.dump(res,file)
    print(res)







from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger



app = FastAPI()
sched = BackgroundScheduler()


@app.get('/')
def http():
    return {'message':'hello world'}

def job_function():
    print('hello world')

sched.add_job(job_function, CronTrigger.from_crontab('*/1 * * * *'))
sched.start()
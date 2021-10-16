

from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from task import fb,tel


app = FastAPI()
sched = BackgroundScheduler()


@app.get('/')
def http():
    return {'message':'hello world'}

def job1():
    tel.sendMessage()

def job2():
    fb.sendMessage(cat="jod")

def job3():
    fb.sendMessage(cat="animal")

def job4():
    fb.sendMessage(cat="blonde")

def job5():
    fb.sendMessage(cat="knock-knock")

sched.add_job(job1, CronTrigger.from_crontab('59 * * * *'))
sched.add_job(job2,CronTrigger.from_crontab('30 2 * * *'))
sched.add_job(job3,CronTrigger.from_crontab('30 4 * * *'))
sched.add_job(job4,CronTrigger.from_crontab('30 6 * * *'))
sched.add_job(job5,CronTrigger.from_crontab('30 8 * * *'))


sched.start()
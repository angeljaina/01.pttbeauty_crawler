import os
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', hour=12)
def scheduled_job():
    os.system("python pttbeautiful.py")  #pttbeautiful.py

sched.start()

from apscheduler.schedulers.blocking import BlockingScheduler

from .email import sendEmailRemainder

sched = BlockingScheduler()

# @sched.scheduled_job('interval', minutes=3)
# def timed_job():
#     print('This job is run every three minutes.')


# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# def scheduled_job():
#     print('This job is run every weekday at 5pm.')

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=8)
def scheduled_job():
    sendEmailRemainder()
    print('This send e-mail every weekday at 8am.')

@sched.scheduled_job('interval', minutes=20)
def timed_job():
    sendEmailRemainder()
    

sched.start()
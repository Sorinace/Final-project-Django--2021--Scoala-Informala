from apscheduler.schedulers.blocking import BackgroundScheduler

from .email import sendEmailRemainder

sched = BackgroundScheduler()

# @sched.scheduled_job('interval', minutes=3)
# def timed_job():
#     print('This job is run every three minutes.')


# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# def scheduled_job():
#     print('This job is run every weekday at 5pm.')

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=7)
def scheduled_job():
    sendEmailRemainder()
    print('This send e-mail every weekday at 7am.')

@sched.scheduled_job('interval', minutes=10)
def timed_job():
    sendEmailRemainder()
    

sched.start()
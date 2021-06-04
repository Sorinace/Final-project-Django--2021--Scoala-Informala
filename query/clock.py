from apscheduler import schedulers

from .email import sendEmailRemainder

sched = schedulers()

# @sched.scheduled_job('interval', minutes=3)
# def timed_job():
#     print('This job is run every three minutes.')


# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# def scheduled_job():
#     print('This job is run every weekday at 5pm.')

@sched.cron_schedule(day_of_week='mon-sun', hour=16, minute=0)
def scheduled_job():
    sendEmailRemainder()
    print('This send e-mail every weekday at 16pm.')

# @sched.scheduled_job('interval', minutes=10)
# def timed_job():
#     sendEmailRemainder()
    

sched.start()
print("Scheduler started")

while __name__ == '__main__':
  pass
from apscheduler.schedulers.blocking import BlockingScheduler

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from smtplib import SMTPException
from rest_framework import serializers

def sendEmailRemainder():
    replay = 'sorinace@gmail.com'

    context = ({"addres": 'www.fess.ro', "data": '25.05.2021', "message": 'Test pentru ENAIL SO'}) 

    text_content = render_to_string('remainder_email.txt', context)
    html_content = render_to_string('remainder_email.html', context)
    
    try:
        #I used EmailMultiAlternatives because I wanted to send both text and html
        emailMessage = EmailMultiAlternatives(subject='Sa nu uitati de TEST', body=text_content, from_email='Testing Schedule', to=['sorinace@gmail.com',], reply_to=[replay,])
        emailMessage.attach_alternative(html_content, "text/html")
        emailMessage.send(fail_silently=False)
    except SMTPException as e:
        print('There was an error sending an email: ', e) 
        error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
        raise serializers.ValidationError(error)

sched = BlockingScheduler()

# @sched.scheduled_job('interval', minutes=3)
# def timed_job():
#     print('This job is run every three minutes.')

# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# def scheduled_job():
#     print('This job is run every weekday at 5pm.')

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=18, minutes=25)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=18, minutes=26)
def scheduled_job():
    sendEmailRemainder()


sched.start()
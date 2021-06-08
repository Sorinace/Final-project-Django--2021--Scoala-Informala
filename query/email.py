from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from smtplib import SMTPException
from rest_framework import serializers
from access_tokens import scope, tokens

from django.conf import settings

def sendEmail(request, subject, assign):
    token = tokens.generate(scope=(), key=settings.SECRET_KEY, salt=settings.TOKEN_SALT) 
    code = f"?token={token}"
    base = "{0}://{1}".format(request.scheme, request.get_host())
    context = ({"addres": f"{base}/query/{assign.id}{code}", "data": assign.data, "message": assign.message}) 

    text_content = render_to_string('receipt_email.txt', context, request=request)
    html_content = render_to_string('receipt_email.html', context, request=request)
    from_us = f"{request.user.first_name} {request.user.last_name}"

    try:
        #I used EmailMultiAlternatives because I wanted to send both text and html
        emailMessage = EmailMultiAlternatives(subject=subject, body=text_content, from_email=from_us, to=[assign.email,], reply_to=[request.user.email,])
        emailMessage.attach_alternative(html_content, "text/html")
        emailMessage.send(fail_silently=False)

    except SMTPException as e:
        print('There was an error sending an email: ', e) 
        error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
        raise serializers.ValidationError(error)


def sendEmailAnswer(request, answer, email):
    if (request.user.is_anonymous):
        replay = 'sorinace@gmail.com'
    else:
        replay = request.user.email

    total = 0
    for item in answer.answer.all():
        total += int(item.choose.score)

    context = ({"answer": answer.answer.all(), "name": answer.name, "total": total}) 

    text_content = render_to_string('receipt_email_answer.txt', context, request=request)
    html_content = render_to_string('receipt_email_answer.html', context, request=request)
    
    try:
        emailMessage = EmailMultiAlternatives(subject='Raspuns la test', body=text_content, from_email='Testing WEB Server', to=[email,], reply_to=[replay,])
        emailMessage.attach_alternative(html_content, "text/html")
        emailMessage.send(fail_silently=False)
    except SMTPException as e:
        print('There was an error sending an email: ', e) 
        error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
        raise serializers.ValidationError(error)

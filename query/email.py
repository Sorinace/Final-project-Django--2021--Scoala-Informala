from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from smtplib import SMTPException
from rest_framework import serializers

def sendEmail(request, subject, email, addres, data, message):
    replay = request.user.email
    

    from_us = f"{request.user.first_name} {request.user.last_name}"

    context = ({"addres":addres, "data": data, "message": message}) #Note I used a normal tuple instead of  Context({"username": "Gilbert"}) because Context is deprecated. When I used Context, I got an error > TypeError: context must be a dict rather than Context

    text_content = render_to_string('receipt_email.txt', context, request=request)
    html_content = render_to_string('receipt_email.html', context, request=request)

    try:
        #I used EmailMultiAlternatives because I wanted to send both text and html
        emailMessage = EmailMultiAlternatives(subject=subject, body=text_content, from_email=from_us, to=[email,], reply_to=[replay,])
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
        # I used EmailMultiAlternatives because I wanted to send both text and html
        emailMessage = EmailMultiAlternatives(subject='Raspuns la test', body=text_content, from_email='Testing WEB Server', to=[email,], reply_to=[replay,])
        emailMessage.attach_alternative(html_content, "text/html")
        emailMessage.send(fail_silently=False)
    except SMTPException as e:
        print('There was an error sending an email: ', e) 
        error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
        raise serializers.ValidationError(error)

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
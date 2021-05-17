from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from smtplib import SMTPException
from rest_framework import serializers


def emailAssignedTest(email, addres, data, mesaj):
  send_mail(
    'Va fost atribuit un test',
    # message
    f"""
    Buna ziua,
        Va rog sa completati testul de la adresa {addres}
        Testul expira in {data}.
        {mesaj}
    O zi frumoasa,
    Diana Avram 
    """,
    'Diana Avram',
    [email], # 'psiholigia@gmail.com'
    fail_silently=False,
  )



def sendEmail(request, subject, email, from_us, addres, data, message):
    replay = "sorinace@gmail.com"

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

def sendEmailAnswer(request, answer):
    replay = "sorinace@gmail.com"

    context = ({"answer": answer, }) 
    text_content = render_to_string('receipt_email_answer.txt', context, request=request)
    html_content = render_to_string('receipt_email_answer.html', context, request=request)
    
    try:
        #I used EmailMultiAlternatives because I wanted to send both text and html
        emailMessage = EmailMultiAlternatives(subject='Raspuns la test', body=text_content, from_email='Server', to=['sorinace@gmail.com',], reply_to=[replay,])
        emailMessage.attach_alternative(html_content, "text/html")
        emailMessage.send(fail_silently=False)
    except SMTPException as e:
        print('There was an error sending an email: ', e) 
        error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
        raise serializers.ValidationError(error)
from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customers
from django.shortcuts import render


def say_hello(request):
    notify_customers.delay()
    # try:
       # send_mail('subject', 'message', recipient_list=['gehikhamhen247@gmail.com'], from_email='info@nicerthings.com.ng')

       # mail_admins('subject', 'message', html_message='mesaage')

       # message = EmailMessage('subject','message', 'from@godwi.com', ['recv@godwin.com'])
       #message.attach_file('playground/static/images/pic.jpg')

    #    message = BaseEmailMessage(
    #     template_name='emails/hello.html',
    #     context={'name':'Godwin '}
    #    )
    #    message.send(to=['john@mosh.com'])
    # except BadHeaderError:
    #     pass

    return render(request, 'hello.html', {'name': 'Mosh'})

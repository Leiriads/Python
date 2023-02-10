import re
from django.contrib import messages
from django.contrib.messages import constants
#emails
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


import smtplib
import email.message



def enviar_email():  
    corpo_email = """
    <a href="www.google.com" style="margin: 0px; outline: none; padding: 14px; color: rgb(255, 255, 255); background: rgb(240, 140, 30); border: 1px solid rgb(240, 140, 30); border-radius: 4px; font-family: Arial; font-size: 16px; display: inline-block; line-height: 1.1; text-align: center; text-decoration: none;"> <span style="color: rgb(255, 255, 255); font-family: Arial; font-size: 16px; font-weight: bold;"> Clique aqui para ir para o Google </span> </a>
    <p> xD </p>
    """

    msg = email.message.Message()
    msg['Subject'] = "Teste"
    msg['From'] = 'leiriads@gmail.com'
    msg['To'] = 'leiriads@gmail.com'
    password = '--' 
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email )

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')











def password_is_valid(request, password, confirm_password):
    if len(password) < 6:
        messages.add_message(request, constants.ERROR, 'Sua senha deve conter 6 ou mais caractertes')
        return False

    if not password == confirm_password:
        messages.add_message(request, constants.ERROR, 'As senhas não coincidem!')
        return False

    if not re.search('[A-Z]', password): 
        messages.add_message(request, constants.ERROR, 'Sua senha não contem letras maiúsculas')
        return False

    if not re.search('[a-z]', password):
        messages.add_message(request, constants.ERROR, 'Sua senha não contem letras minúsculas')
        return False

    if not re.search('[1-9]', password):
        messages.add_message(request, constants.ERROR, 'Sua senha não contém números')
        return False
    return True


def email_html(path_template: str, assunto: str, para: list, **kwargs) -> dict:
    html_content = render_to_string(path_template, kwargs)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(assunto, text_content, settings.EMAIL_HOST_USER, para)
    email.attach_alternative(html_content, "text/html")
    email.send()
    return {'status': 1}




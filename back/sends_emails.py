import mimetypes
import smtplib as sl
import os
from email import encoders

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase


def send_email(message):
    sender = 'bymworking@gmail.com'
    password = 'lvuqbqehjxfnfwiy'
    server = sl.SMTP('smtp.gmail.com', 587)
    server.starttls()
    try:
        server.login(sender, password)
        msg = MIMEMultipart()
        msg['SUBJECT'] = 'Новый заказ!'
        msg.attach(MIMEText(message))
        for file in os.listdir('uploads'):
            filename = os.path.basename(file)
            ftype, encoding = mimetypes.guess_type(file)
            file_type, subtype = ftype.split('/')

            if file_type == 'text':
                with open(f"uploads/{file}") as f:
                    file = MIMEText(f.read())
            elif file_type == 'image':
                with open(f"uploads/{file}", 'rb') as f:
                    file = MIMEImage(f.read(), subtype)
            else:
                with open(f"uploads/{file}", "rb") as f:
                    file = MIMEBase(file_type, subtype)
                    file.set_payload(f.read())
                    encoders.encode_base64(file)

            file.add_header('content-disposition', 'attachment', filename=filename)
            msg.attach(file)
            os.remove(f'uploads/{filename}')
        server.sendmail(sender, 'bymworking@gmail.com', msg.as_string())
        return 'The massage was sent successful!'
    except Exception as ex:
        return f"{ex} \n Check your login or password, please!"


def send_emal_to_user(messag, email, n):
    sender = 'bymworking@gmail.com'
    password = 'lvuqbqehjxfnfwiy'
    server = sl.SMTP('smtp.gmail.com', 587)
    server.starttls()
    try:
        server.login(sender, password)
        msg = MIMEText(messag)
        if n == 1:
            msg['SUBJECT'] = 'Ваш заказ зарегистрирован'
        else:
            msg['SUBJECT'] = 'Информация об аккаунте'
        server.sendmail(sender, email, msg.as_string())
        return 'The message was sent successful!'
    except Exception as ex:
        return f"{ex} \n Check your password"


print(send_email('Misha_test'))

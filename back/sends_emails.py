import smtplib as sl
from email.mime.text import MIMEText


def send_email(message):
    sender = 'bymworking@gmail.com'
    password = 'lvuqbqehjxfnfwiy'
    server = sl.SMTP('smtp.gmail.com', 587)
    server.starttls()
    try:
        server.login(sender, password)
        msg = MIMEText(message)
        msg['SUBJECT'] = 'Новый заказ!'
        server.sendmail(sender, 'bymworking@gmail.com', msg.as_string())
        return 'The massage was sent successful!'
    except Exception as ex:
        return f"{ex} \n Check your login or password, please!"

#
# print(send('Misha_test'))

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Length


class Make_Serv(FlaskForm):
    number = StringField("Телефонный номер")
    about_serv = StringField(validators=[Length(max=100)])
    upload = SubmitField('Отправить')


class Name_of_serv(FlaskForm):
    service = StringField()


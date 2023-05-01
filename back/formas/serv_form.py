from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Length


class Make_Serv(FlaskForm):
    service = SelectField("Выбрать услугу")
    number = StringField("Телефонный номер")
    about_serv = StringField(validators=[Length(max=100)])
    upload = SubmitField('Отправить')


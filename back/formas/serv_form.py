from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length


class Make_Serv(FlaskForm):
    service = StringField("Выбрать услугу")
    about_serv = StringField(validators=[Length(max=1000)])
    upload = SubmitField('Отправить')


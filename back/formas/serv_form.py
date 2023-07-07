from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, DataRequired


class Make_Serv(FlaskForm):
    number = StringField("Телефонный номер", validators=[DataRequired()])
    about_serv = StringField(validators=[Length(max=100)])
    upload = SubmitField('Отправить')





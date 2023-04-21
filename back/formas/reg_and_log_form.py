from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length


class Reg_form(FlaskForm):
    name = StringField("Ваше имя:", validators=[Length(min=2)])
    surname = StringField("Ваша фамилия:",validators=[Length(min=2)])
    email = StringField()
    password = PasswordField()
    Reg_submit = StringField('Зарегистрироваться')


class Login_form(FlaskForm):
    email = StringField()
    password = PasswordField()
    log_sub = SubmitField("Войти")






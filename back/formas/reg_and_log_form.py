from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length


class Reg_form(FlaskForm):
    name = StringField("Ваше имя:", validators=[Length(min=2)])
    surname = StringField("Ваша фамилия:", validators=[Length(min=2)])
    email = StringField("Почта")
    password = PasswordField('Пароль')
    Reg_submit = SubmitField('Зарегистрироваться')


class Login_form(FlaskForm):
    email = StringField("Почта")
    password = PasswordField('Пароль')
    log_sub = SubmitField("Войти")

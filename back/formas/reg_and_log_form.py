from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length


class Reg_form(FlaskForm):
    login = StringField("Ваше имя:", validators=[Length(min=2)])
    email = StringField("Почта")
    password = PasswordField('Пароль')
    Reg_submit = SubmitField('Зарегистрироваться')


class Login_form(FlaskForm):
    login = StringField("Логин")
    password = PasswordField('Пароль')
    log_sub = SubmitField("Войти")

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators


class Reg_form(FlaskForm):
    name = StringField("Ваше имя:", [validators.DataRequired(), validators.Length(min=2, max=30)])
    surname = StringField("Ваша фамилия", [validators.DataRequired()])
    email = StringField("Почта", [validators.DataRequired(), validators.Email()])
    password = PasswordField('Пароль', [validators.DataRequired()])
    Reg_submit = SubmitField('Зарегистрироваться')


class Login_form(FlaskForm):
    email = StringField("Почта", [validators.DataRequired(), validators.Email()])
    password = PasswordField('Пароль', [validators.DataRequired()])
    log_sub = SubmitField("Войти")

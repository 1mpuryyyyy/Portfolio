from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import Length
from back.main import photos




class Make_Serv(FlaskForm):
    service = SelectField("Выбрать услугу")
    number = StringField("Телефонный номер")
    about_serv = StringField(validators=[Length(max=100)])
    photo = FileField(validators=[FileAllowed(photos), FileRequired('File files should bo not empty')])
    upload = SubmitField('Отправить')


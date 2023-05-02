from peewee import *

db = SqliteDatabase('C:/Users/Misha/PycharmProjects/Portfoli/back/database.db')


class Base_Model(Model):  # Базовый класс
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order_by = 'id'


class User(Base_Model):  # Наследуемся от базового класса
    login = CharField()
    email = CharField()

    class Meta:
        database = db
        order_by = 'id'
        db_table = 'peoples_data_reg'

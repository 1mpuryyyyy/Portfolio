import sqlalchemy as db
from .db_session import SqlAlchemyBase

from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    id_serv = db.Column(db.Integer, nullable=False, default=1)
    email = db.Column(db.String(64), nullable=True, unique=True, index=True)
    name = db.Column(db.String(32), nullable=False)
    surname = db.Column(db.String(32), nullable=False)
    hashed_password = db.Column(db.String, nullable=False)



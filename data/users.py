import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from datetime import time


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    telegram_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, unique=True)
    time = sqlalchemy.Column(sqlalchemy.Time, default=time(12, 00, 00))
    classes = sqlalchemy.Column(sqlalchemy.Integer)

    olimp = orm.relationship('Relation')
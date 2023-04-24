import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from datetime import time


class User(SqlAlchemyBase):  # таблица с пользователями
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    telegram_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, unique=True)  # id в телеграме

    # использование в других таблицах
    olimp = orm.relationship('Relation')

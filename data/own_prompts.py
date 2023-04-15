import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from datetime import time


class OwnPrompts(SqlAlchemyBase):
    __tablename__ = 'own_prompts'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    date = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    time = sqlalchemy.Column(sqlalchemy.Time, default=time(12, 00, 00))

    user = orm.relationship('User')

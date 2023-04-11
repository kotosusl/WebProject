import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Olimp(SqlAlchemyBase):
    __tablename__ = 'olimpycs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, unique=True)

    user = orm.relationship('User')

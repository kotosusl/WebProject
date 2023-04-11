import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Relation(SqlAlchemyBase):
    __tablename__ = 'user_olimpyc'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    olimp = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('olimpycs.id'), nullable=False)


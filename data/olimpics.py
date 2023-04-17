import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Olimp(SqlAlchemyBase):
    __tablename__ = 'olimpycs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    href = sqlalchemy.Column(sqlalchemy.String)
    desc = sqlalchemy.Column(sqlalchemy.TEXT)
    min_class = sqlalchemy.Column(sqlalchemy.Integer)
    max_class = sqlalchemy.Column(sqlalchemy.Integer)

    user = orm.relationship('Relation')
    subject = orm.relationship('Olimp_Subject')
    dates = orm.relationship('Olimp_dates')


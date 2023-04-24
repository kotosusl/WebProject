import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Olimp(SqlAlchemyBase):  # таблица с олимпиадами
    __tablename__ = 'olimpycs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)  # название олимпиады
    href = sqlalchemy.Column(sqlalchemy.String)  # ссылка
    desc = sqlalchemy.Column(sqlalchemy.TEXT)  # описание
    min_class = sqlalchemy.Column(sqlalchemy.Integer)  # минимальный класс для участия
    max_class = sqlalchemy.Column(sqlalchemy.Integer)  # максимальный класс для участия

    # использование в других таблицах
    user = orm.relationship('Relation')
    subject = orm.relationship('Olimp_Subject')
    dates = orm.relationship('Olimp_dates')

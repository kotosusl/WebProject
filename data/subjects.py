import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Subject(SqlAlchemyBase):  # таблица с предметами
    __tablename__ = 'subjects'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)  # название предмета

    # использование в других таблицах
    olimp = orm.relationship('Olimp_Subject')

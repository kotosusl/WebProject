import sqlalchemy
from .db_session import SqlAlchemyBase


class Olimp_Subject(SqlAlchemyBase):  # таблица "многие ко многим", связь олимпиады с предметами
    __tablename__ = 'olimp_subject'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    subject = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('subjects.id'), nullable=False)  # предмет
    olimp = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('olimpycs.id'), nullable=False)  # олимпиада

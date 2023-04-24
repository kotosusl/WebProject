import sqlalchemy
from .db_session import SqlAlchemyBase


class Olimp_dates(SqlAlchemyBase):  # таблица "один ко многим", связь олимпиад с проводимыми этапами
    __tablename__ = 'olimp_dates'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    olimp = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('olimpycs.id'), nullable=False)  # олимпиада
    start_date = sqlalchemy.Column(sqlalchemy.Date, nullable=False)  # дата начала этапа
    end_date = sqlalchemy.Column(sqlalchemy.Date, nullable=False)  # дата конца этапа
    event = sqlalchemy.Column(sqlalchemy.String)  # название этапа

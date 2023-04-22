import sqlalchemy
from .db_session import SqlAlchemyBase


class Olimp_dates(SqlAlchemyBase):
    __tablename__ = 'olimp_dates'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    olimp = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('olimpycs.id'), nullable=False)
    start_date = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    end_date = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    event = sqlalchemy.Column(sqlalchemy.String)

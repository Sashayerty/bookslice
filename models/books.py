import datetime

import sqlalchemy

from .db_session import SqlAlchemyBase


class Books(SqlAlchemyBase):
    __tablename__ = "books"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )  # noqa
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # noqa
    author = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    writed_in = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    count_of_words = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    speed_of_reading = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    created_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now, nullable=False
    )  # noqa

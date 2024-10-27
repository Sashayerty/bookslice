import datetime

import sqlalchemy
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = "user"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )  # noqa
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(
        sqlalchemy.String, unique=True, nullable=False
    )  # noqa
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    speed_of_reading = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    created_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now
    )  # noqa

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

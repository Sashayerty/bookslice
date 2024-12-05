import datetime

import sqlalchemy
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .db_session import SqlAlchemyBase


class Users(SqlAlchemyBase, UserMixin):
    """Модель юзера"""

    __tablename__ = "users"

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
    )
    name = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
    )
    email = sqlalchemy.Column(
        sqlalchemy.String,
        unique=True,
        nullable=False,
    )
    hashed_password = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
    )
    speed_of_reading = sqlalchemy.Column(
        sqlalchemy.Integer,
        nullable=True,
    )
    created_date = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=datetime.datetime.now,
    )
    admin = sqlalchemy.Column(
        sqlalchemy.Boolean,
        default=False,
    )
    read_books = sqlalchemy.Column(
        sqlalchemy.Integer,
        default=0,
    )
    summarized_books = sqlalchemy.Column(
        sqlalchemy.Integer,
        default=0,
    )

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def get_data(self) -> dict:
        """Возвращает данные о прочитанных книгах и сжатых книгах (ТОЛЬКО количество)

        Returns:
            dict[str[dict[str[int]]]]: словарь значений типа {'data': {'read-books': int, 'summarized_books': int}}
        """
        return {
            "data": {
                "read_books": self.read_books,
                "summarized_books": self.summarized_books,
            }
        }

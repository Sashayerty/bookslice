import sqlalchemy

from .db_session import SqlAlchemyBase


class Books(SqlAlchemyBase):
    """Модель книг"""

    __tablename__ = "books"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )  # noqa
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    author = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    writed_in = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    count_of_words = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    original = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
    genere = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

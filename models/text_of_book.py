import sqlalchemy

from .db_session import SqlAlchemyBase


class TextOfBook(SqlAlchemyBase):
    """Модель текста книги"""

    __tablename__ = "text_of_book"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    book_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    text = sqlalchemy.Column(sqlalchemy.Text, nullable=False)

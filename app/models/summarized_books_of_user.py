import sqlalchemy

from .db_session import SqlAlchemyBase


class SummarizedBooksOfUser(SqlAlchemyBase):
    __tablename__ = "summarized_books_of_user"

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
    )
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        nullable=False,
    )
    book_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        nullable=False,
    )
    text = sqlalchemy.Column(
        sqlalchemy.Text,
        nullable=False,
    )

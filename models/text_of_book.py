import sqlalchemy

from .db_session import SqlAlchemyBase


class TextOfBook(SqlAlchemyBase):
    __tablename__ = "text_of_book"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    book_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("books.id"), nullable=False
    )  # noqa
    text = sqlalchemy.Column(sqlalchemy.String, nullable=False)

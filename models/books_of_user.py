import sqlalchemy

from .db_session import SqlAlchemyBase


class BooksOfUser(SqlAlchemyBase):
    __tablename__ = "books_of_user"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    book_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    status = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

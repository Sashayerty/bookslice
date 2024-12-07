import sqlalchemy

from .db_session import SqlAlchemyBase


class TestsOfUser(SqlAlchemyBase):
    __tablename__ = "tests_of_user"

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
    )
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        nullable=False,
    )
    summarized_book_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        nullable=False,
    )
    test = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
    )

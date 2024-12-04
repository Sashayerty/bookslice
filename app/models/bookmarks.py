import sqlalchemy

from .db_session import SqlAlchemyBase


class BookMarks(SqlAlchemyBase):
    """Модель закладок пользователей"""

    __tablename__ = "bookmarks"

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
    page = sqlalchemy.Column(
        sqlalchemy.Integer,
        nullable=False,
    )

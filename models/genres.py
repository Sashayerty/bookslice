import sqlalchemy

from .db_session import SqlAlchemyBase


class Genres(SqlAlchemyBase):
    """Модель жанров"""

    __tablename__ = "genres"

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
    )
    name = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
        unique=True,
    )
    en_name = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
        unique=True,
    )

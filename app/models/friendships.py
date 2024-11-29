import sqlalchemy

from .db_session import SqlAlchemyBase


class Friendships(SqlAlchemyBase):
    """Модель друзей"""

    __tablename__ = "friendships"

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
    )
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        nullable=False,
        unique=True,
    )
    friends_ids = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
    )

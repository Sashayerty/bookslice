import sqlalchemy

from .db_session import SqlAlchemyBase


class FriendRequests(SqlAlchemyBase):
    """Модель запроса в друзья"""

    __tablename__ = "friend_requests"

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

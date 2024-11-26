import sqlalchemy

from .db_session import SqlAlchemyBase


class Notifications(SqlAlchemyBase):
    """Модель уведомлений"""

    __tablename__ = "notifications"

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
    )
    type = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
    )
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        nullable=False,
    )
    data = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
    )

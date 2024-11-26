import sqlalchemy

from .db_session import SqlAlchemyBase


class AchievementsOfUsers(SqlAlchemyBase):
    """Модель ачивок юзеров"""

    __tablename__ = "achievements_of_users"

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
    )
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        nullable=False,
    )
    achievement_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        nullable=False,
    )

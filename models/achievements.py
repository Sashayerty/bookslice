import sqlalchemy

from .db_session import SqlAlchemyBase


class Achievements(SqlAlchemyBase):
    """Модель ачивок.
    type: `str`,
    condition: `int`
    ## Example:
    'type' = 'pages',
    'condition' = 100"""

    __tablename__ = "achievements"

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
    )
    title = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
    )  # название ачивки
    description = sqlalchemy.Column(
        sqlalchemy.Text,
        nullable=False,
    )  # описание ачивки
    type = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
    )  # тип ачивки
    condition = sqlalchemy.Column(
        sqlalchemy.Integer,
        nullable=False,
    )  # условие по типу
    reward = sqlalchemy.Column(
        sqlalchemy.Integer,
        nullable=False,
    )  # баллы

import sqlalchemy
from .db_session import SqlAlchemyBase


class Authors(SqlAlchemyBase):
    __tablename__ = "authors"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.Text, nullable=False)

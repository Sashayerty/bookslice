import sqlalchemy

from .db_session import SqlAlchemyBase


class Generes(SqlAlchemyBase):
    __tablename__ = "generes"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)

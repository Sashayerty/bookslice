import sqlalchemy
from .db_session import SqlAlchemyBase


class DescriptionOfUser(SqlAlchemyBase):
    __tablename__ = "description_of_user"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.ForeignKey("books.id"), nullable=False) # noqa
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)

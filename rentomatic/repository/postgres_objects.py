import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Room(Base):
    __tablename__ = "room"

    id = sql.Column(sql.Integer, primary_key=True)

    code = sql.Column(sql.String(36), nullable=False)
    size = sql.Column(sql.Integer)
    price = sql.Column(sql.Integer)
    longitude = sql.Column(sql.Float)
    latitude = sql.Column(sql.Float)

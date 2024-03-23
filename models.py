from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

from engine import engine

Base = declarative_base()


class Cache(Base):
    __tablename__ = "cache_table"

    hash = Column(String(100), primary_key=True)
    path = Column(String(200))


Base.metadata.create_all(engine)

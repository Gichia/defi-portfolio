import os

from sqlmodel import create_engine

SQLALCHEMY_DATABASE_URI = os.environ('SQLALCHEMY_DATABASE_URI')

engine = create_engine(str(SQLALCHEMY_DATABASE_URI))

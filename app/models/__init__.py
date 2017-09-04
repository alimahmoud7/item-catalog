from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

from .field import Field  # noqa
from .mooc import MOOC  # noqa
from .user import User  # noqa

engine = create_engine('postgresql://catalog:123534@localhost/catalog')

Base.metadata.create_all(engine)

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

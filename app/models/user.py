from sqlalchemy import Column, Integer, String
from app.models import Base


class User(Base):
    """Represent a logged in user
    to create local permission system for users"""
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

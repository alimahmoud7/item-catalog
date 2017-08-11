from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class Field(Base):
    """Represent a field in Computer Science"""
    __tablename__ = 'field'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id':   self.id,
            'name': self.name
        }


class MOOC(Base):
    """Represent an online course exists in a MOOC provider"""
    __tablename__ = 'mooc'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    provider = Column(String(80), nullable=False)
    creator = Column(String(80))
    level = Column(String(32))
    description = Column(String(250))
    cost = Column(String(10))
    link = Column(String(250))
    image = Column(String(250))
    field_id = Column(Integer, ForeignKey('field.id'))
    field = relationship("Field")

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id':           self.id,
            'title':        self.title,
            'provider':     self.provider,
            'creator':      self.creator,
            'level':        self.level,
            'description':  self.description,
            'cost':         self.cost,
            'link':         self.link,
            'image':        self.image
        }


engine = create_engine('sqlite:///top_mooc.db')

Base.metadata.create_all(engine)

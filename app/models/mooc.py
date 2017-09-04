from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base


class MOOC(Base):
    """Represent an online course exists in a MOOC provider"""
    __tablename__ = 'mooc'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    provider = Column(String(80), nullable=False)
    creator = Column(String(80))
    level = Column(String(32))
    url = Column(String(250))
    description = Column(String(250))
    image = Column(String(250))
    field_id = Column(Integer, ForeignKey('field.id'))
    field = relationship("Field")
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User")

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
            'url':          self.url,
            'image':        self.image,
            'field_id':     self.field_id
        }

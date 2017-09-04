from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base


class Field(Base):
    """Represent a field in Computer Science"""
    __tablename__ = 'field'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User")

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id':   self.id,
            'name': self.name
        }

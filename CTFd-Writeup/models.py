from CTFd.models import db
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, Text, Boolean, Column, ForeignKey


class WriteupModel(db.Model):
    __tablename__ = "writeups"
    id = Column(Integer, ForeignKey('challenges.id', ondelete="CASCADE"), primary_key=True)
    content = Column(Text)
    visible = Column(Boolean, default=False)
    challenge = relationship('Challenges', uselist=False, backref='writeups')

    def __init__(self, id, content, visible):
        self.id = id
        self.content = content
        self.visible = visible

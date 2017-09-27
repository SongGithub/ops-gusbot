"""TODO"""
from sqlalchemy import Column, Integer, String
from model.database import BASE

class Channel(BASE):
    """TODO"""
    __tablename__ = 'channel'

    channel_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    user = Column(String(50))

    def __repr__(self):
        return "<Channel(name='%s', user='%s')>" % (self.name, self.user)

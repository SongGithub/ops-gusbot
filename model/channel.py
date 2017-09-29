"""TODO"""
from sqlalchemy import Column, Integer, String
from model.database import BASE

class Channel(BASE):
    """TODO"""
    __tablename__ = 'whitelist_rules'

    primary_key     = Column(Integer, primary_key=True)
    channel_name    = Column(String(50))
    channel_id      = Column(String(50))
    user_id         = Column(String(50))

    def __repr__(self):
        return "<Channel(name='%s', user='%s')>" % (self.channel_name, self.user_id)

""" SQLAlchemy Wrapper for Database """

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

ENGINE = create_engine("sqlite:///gus-bot.db", convert_unicode=True)
SESSION = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=ENGINE))

BASE = declarative_base()
BASE.query = SESSION.query_property()

def init_db():
    """Initialize database"""
    import model.channel
    BASE.metadata.create_all(bind=ENGINE)

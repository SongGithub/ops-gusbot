""" SQLAlchemy Wrapper for Database """
import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

LOGGER = logging.getLogger(__name__)

DB = os.getenv("SLACKBOT_DATABASE", "sqlite:///gus-bot.db")

ENGINE = create_engine(DB, convert_unicode=True)
SESSION = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=ENGINE))

BASE = declarative_base()
BASE.query = SESSION.query_property()

def init_db():
    """Initialize database"""
    import model.channel
    LOGGER.info("Initializing Dababase")
    BASE.metadata.create_all(bind=ENGINE)

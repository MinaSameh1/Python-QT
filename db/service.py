"""Responsible for everything related to sqlite itself."""


from sqlalchemy import create_engine, event, DDL
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base


class Db:
    """Singleton DB class, responsible for all basic sqlite operations."""

    __instance = None

    engine = None
    session: Session
    Base = declarative_base()

    @staticmethod
    def get_instance():
        """Get instance of class."""
        if Db.__instance is None:
            Db()
        return Db.__instance

    def __init__(self):
        """Do not create multiple objects."""
        if Db.__instance is not None:
            raise Exception(
                "This is a singleton, found attempt to create multiple of it."
            )

    @staticmethod
    def connect():
        """Connect to db."""
        try:
            if Db.engine is None:
                Db.engine = create_engine("sqlite:///task.db", echo=True)
                db_session = sessionmaker(bind=Db.engine)
                Db.session = db_session()
                Db.create_tables()
        except Exception as err:
            print("error in connect: ", err)

    @staticmethod
    def create_tables():
        """Create Tables."""
        Db.Base.metadata.create_all(Db.engine)
        Db.session.commit()

    @staticmethod
    def get_session():
        """Return Session created by session maker."""
        return Db.session

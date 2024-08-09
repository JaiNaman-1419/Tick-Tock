from config import SqliteConfig
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


SQLALCHEMY_DATABASE_URL = SqliteConfig().get_database_url

ENGINE = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

SESSION_LOCAL = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)

BASE = declarative_base()


class Database:
    db = SESSION_LOCAL()

    @classmethod
    def get_db(cls):
        try:
            yield cls.db
        finally:
            cls.db.close()

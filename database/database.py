from config import MySqlConfig
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# Database URL for Postgresql, import it from config.
# SQLALCHEMY_DATABASE_URL = PostgresConfig().get_database_url           
SQLALCHEMY_DATABASE_URL = MySqlConfig().get_database_url           

ENGINE = create_engine(SQLALCHEMY_DATABASE_URL)
# Engine for SQLite only.
# ENGINE = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

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

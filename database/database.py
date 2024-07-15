from pathlib import Path
from os.path import join as pathjoiner
from sqlalchemy import create_engine
from configparser import ConfigParser
from sqlalchemy.orm import sessionmaker, declarative_base


config = ConfigParser()
config_file_path = Path(__file__).resolve().parent.parent
config_file = pathjoiner(config_file_path, 'config', 'config.ini')
config.read(config_file)


SQLALCHEMY_DATABASE_URL = config['database']['database_url']

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

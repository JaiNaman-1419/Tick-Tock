from pathlib import Path
from os.path import join as pathjoiner
from configparser import ConfigParser


class BaseConfig:
    _CONFIG = ConfigParser()
    __CONFIG_FILE_PATH = Path(__file__).resolve().parent
    __CONFIG_FILE = pathjoiner(__CONFIG_FILE_PATH, "config", "config.ini")
    _CONFIG.read(__CONFIG_FILE)


class DatabaseConfig(BaseConfig):

    @property
    def get_database_name(self):
        return self._CONFIG["database"]["database_name"]

    @property
    def get_user_table_name(self):
        return self._CONFIG["database"]["user_table_name"]

    @property
    def get_todo_table_name(self):
        return self._CONFIG["database"]["todo_table_name"]


class PostgresConfig(BaseConfig):

    @property
    def get_database_url(self):
        host = self._CONFIG["postgres"]["host"]
        username = self._CONFIG["postgres"]["username"]
        password = self._CONFIG["postgres"]["password"]

        return f"postgresql://{username}:{password}@{host}/{DatabaseConfig().get_database_name}"


class MySqlConfig(BaseConfig):

    @property
    def get_database_url(self):
        host = self._CONFIG["mysql"]["host"]
        username = self._CONFIG["mysql"]["username"]
        password = self._CONFIG["mysql"]["password"]

        return f"mysql+pymysql://{username}:{password}@{host}/{DatabaseConfig().get_database_name}"


class SqliteConfig(BaseConfig):

    @property
    def get_database_url(self):
        return self._CONFIG["sqlite"]["database_url"]

    @property
    def get_database_file(self):
        return self._CONFIG["sqlite"]["database_file"]


class JwtConfig(BaseConfig):

    @property
    def get_encoding_algorithm(self):
        return self._CONFIG["jwt"]["algorithm"]

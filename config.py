from pathlib import Path
from os.path import join as pathjoiner
from configparser import ConfigParser


class BaseConfig:
    _CONFIG = ConfigParser()
    __CONFIG_FILE_PATH = Path(__file__).resolve().parent
    __CONFIG_FILE = pathjoiner(__CONFIG_FILE_PATH, "config", "config.ini")
    _CONFIG.read(__CONFIG_FILE)


class SqliteConfig(BaseConfig):

    @property
    def get_user_table_name(self):
        return self._CONFIG["sqlite"]["user_table_name"]

    @property
    def get_todo_table_name(self):
        return self._CONFIG["sqlite"]["todo_table_name"]

    @property
    def get_database_url(self):
        return self._CONFIG["sqlite"]["database_url"]

    @property
    def get_database_file_name(self):
        return self._CONFIG["sqlite"]["database_file_name"]


class JwtConfig(BaseConfig):

    @property
    def get_encoding_algorithm(self):
        return self._CONFIG["jwt"]["algorithm"]

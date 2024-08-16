from database import BASE
from config import SqliteConfig
from sqlalchemy import (
    Column, Integer,
    String, Boolean
)


class Users(BASE):
    __tablename__ = SqliteConfig().get_user_table_name

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

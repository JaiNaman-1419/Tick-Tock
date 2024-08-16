from database import BASE
from .users_model import Users
from config import SqliteConfig
from sqlalchemy import (
    Column, Integer,
    String, Boolean,
    ForeignKey, Text
)


class Todos(BASE):
    __tablename__ = SqliteConfig().get_todo_table_name

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey(f"{SqliteConfig().get_user_table_name}.id"))

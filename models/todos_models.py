from database import BASE
from .users_model import Users
from config import DatabaseConfig

from sqlalchemy import (
    Column, Integer,
    String, Boolean,
    ForeignKey, Text
)


class Todos(BASE):
    __tablename__ = DatabaseConfig().get_todo_table_name

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey(f"{DatabaseConfig().get_user_table_name}.id"))

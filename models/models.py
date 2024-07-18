from database import BASE
from config import SqliteConfig
from sqlalchemy import (
    Column, Integer,
    String, Boolean
)


class Todos(BASE):
    __tablename__ = SqliteConfig().get_todo_table_name

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)

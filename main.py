import os
from pathlib import Path
from os.path import isfile
from fastapi import FastAPI
from routers import get_todos_api
from database.migrations import create_database


app = FastAPI()
path = Path(__file__).resolve().parent
db_file = os.path.join(path, 'todos.db')


if not isfile(db_file):
    create_database()

app.include_router(get_todos_api.ROUTER)

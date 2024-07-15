import routers
from pathlib import Path
from os.path import isfile
from fastapi import FastAPI
from os.path import join as pathjoiner
from database.migrations import create_database


app = FastAPI()
path = Path(__file__).resolve().parent
db_file = pathjoiner(path, 'todos.db')


if not isfile(db_file):
    create_database()

app.include_router(routers.get_todo_router)
app.include_router(routers.create_todo_router)

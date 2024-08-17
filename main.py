import auth
from pathlib import Path
from os.path import isfile
from fastapi import FastAPI

from os.path import join as pathjoiner
from database.migrations import create_database
from admin.base_api import ROUTER as admin_router
from routers.base_api import ROUTER as todo_router


app = FastAPI()
path = Path(__file__).resolve().parent
# db_file = pathjoiner(path, SqliteConfig().get_database_file_name)


# if not isfile(db_file):
#     create_database()


app.include_router(todo_router)
app.include_router(admin_router)
app.include_router(auth.auth_router)

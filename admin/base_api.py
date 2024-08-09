from auth import Token
from typing import Annotated
from database import Database
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter


ROUTER = APIRouter(prefix="/admin/todos", tags=["admin"])


class BaseApi:
    _DB_DEPENDENCY = Annotated[Session, Depends(Database.get_db)]
    _OAUTH_DEPENDENCY = Annotated[dict, Depends(Token().get_current_user)]

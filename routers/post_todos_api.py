from typing import Annotated
from models.models import Todos
from fastapi_utils.cbv import cbv

from sqlalchemy.orm import Session
from database.database import Database
from validations.models import TodoModel, ListTodoModel

from fastapi import (
    status, Depends,
    APIRouter, HTTPException
)


ROUTER = APIRouter(prefix="/todos", tags=["TODO"])


@cbv(ROUTER)
class PostTodoApi:
    db_dependency = Annotated[Session, Depends(Database.get_db)]

    @ROUTER.post(
        path="/create",
        response_model=ListTodoModel,
        status_code=status.HTTP_201_CREATED,
    )
    async def create_todos_list(
        self,
        db: db_dependency,
        todo_request: TodoModel,
    ):
        todo_model = Todos(**todo_request.model_dump())
        
        db.add(todo_model)
        db.commit()

        return ListTodoModel(
            id=todo_model.id,
            data=todo_request
        )

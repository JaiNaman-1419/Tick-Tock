from models import Todos
from typing import Annotated
from httpx import AsyncClient
from database import Database

from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from .get_todos_api import GetTodoApi
from validations import TodoModel, ListTodoModel

from fastapi import (
    Path, status, Depends,
    APIRouter, HTTPException
)


ROUTER = APIRouter(prefix="/todos", tags=["TODO"])


@cbv(ROUTER)
class PutTodoApi:
    db_dependency = Annotated[Session, Depends(Database.get_db)]

    @ROUTER.put(
        path="/edit/{todo_id}",
        response_model=ListTodoModel,
        status_code=status.HTTP_200_OK,
    )
    async def edit_todos_list(
        self,
        db: db_dependency,
        todo_request: TodoModel,
        todo_id: int = Path(gt=0),
    ):
        todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
        if todo_model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found :("
            )
        
        todo_model.title = todo_request.title
        todo_model.description = todo_request.description
        todo_model.priority = todo_request.priority
        todo_model.complete = todo_request.complete

        db.add(todo_model)
        db.commit()

        return await GetTodoApi().get_todo_by_id(db, todo_id=todo_id)

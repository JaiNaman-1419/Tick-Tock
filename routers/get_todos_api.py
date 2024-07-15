from typing import List
from typing import Annotated
from models.models import Todos
from fastapi_utils.cbv import cbv

from sqlalchemy.orm import Session
from database.database import Database
from validations.models import TodoModel, ListTodoModel

from fastapi import (
    Path, status, 
    APIRouter, Depends,
    HTTPException
)


ROUTER = APIRouter(prefix='/todos', tags=["TODO"])


@cbv(ROUTER)
class GetTodoApi:
    db_dependency = Annotated[Session, Depends(Database.get_db)]

    @ROUTER.get(
        path='/list',
        status_code=status.HTTP_200_OK,
        response_model=List[ListTodoModel],
    )
    async def get_todos_list(self, db: db_dependency):
        todos = db.query(Todos).all()

        return [
            ListTodoModel(
                id=todo.id,
                data=TodoModel(
                    title=todo.title,
                    description=todo.description,
                    priority=todo.priority,
                    complete=todo.complete,
                )
            )
            for todo in todos
        ]

    @ROUTER.get(
        path='/list/{todo_id}',
        response_model=ListTodoModel,
        status_code=status.HTTP_200_OK,
    )
    async def get_todo_by_id(self, db: db_dependency, todo_id: int = Path(gt=0)):
        todo = db.query(Todos).filter(Todos.id == todo_id).first()

        if todo is not None:
            return ListTodoModel(
                id=todo.id,
                data=TodoModel(
                    title=todo.title,
                    description=todo.description,
                    priority=todo.priority,
                    complete=todo.complete,
                )
            )
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo item not found"
        )

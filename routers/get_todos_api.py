from typing import List
from typing import Annotated
from models.models import Todos
from fastapi_utils.cbv import cbv

from sqlalchemy.orm import Session
from database.database import Database
from validations.models import ListTodoModel

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
        return db.query(Todos).all()

    @ROUTER.get(
        path='/list/{todo_id}',
        response_model=ListTodoModel,
        status_code=status.HTTP_200_OK,
    )
    async def get_todo_by_id(self, db: db_dependency, todo_id: int = Path(gt=0)):
        todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

        if todo_model is not None:
            return todo_model
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo item not found"
        )

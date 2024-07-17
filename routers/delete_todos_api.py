from typing import List
from models import Todos
from typing import Annotated
from database import Database

from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from fastapi import (
    Path, status, 
    APIRouter, Depends,
    HTTPException
)


ROUTER = APIRouter(prefix='/todos', tags=["TODO"])


@cbv(ROUTER)
class DeleteTodoApi:
    db_dependency = Annotated[Session, Depends(Database.get_db)]

    @ROUTER.delete(
        path='/delete/{todo_id}',
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def delete_todo_item(
        self,
        db: db_dependency,
        todo_id: int = Path(gt=0)
    ):
        todo = db.query(Todos).filter(Todos.id == todo_id).first()
        if todo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found :("
            )
        
        if db.query(Todos).filter(Todos.id == todo_id).delete():
            db.commit()
            return
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something goes wrong :|"
        )

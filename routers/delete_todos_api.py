from models import Todos
from fastapi_utils.cbv import cbv
from .base_api import BaseApi, ROUTER
from fastapi import Path, status, HTTPException


@cbv(ROUTER)
class DeleteTodoApi(BaseApi):

    @ROUTER.delete(
        path='/delete/{todo_id}',
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def delete_todo_item(
        self,
        db: BaseApi._DB_DEPENDENCY,
        user: BaseApi._OAUTH_DEPENDENCY,
        todo_id: int = Path(gt=0)
    ):
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication Failed :("
            )

        todo = db.query(Todos).filter(
            Todos.id == todo_id
        ).filter(
            Todos.owner_id == user.get("id")
        ).first()

        if todo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found :("
            )
        
        if db.query(Todos).filter(
                Todos.id == todo_id
            ).filter(
                Todos.owner_id == user.get("id")
            ).delete():
            db.commit()
            return
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something goes wrong :|"
        )

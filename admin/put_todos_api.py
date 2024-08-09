from models import Todos
from fastapi_utils.cbv import cbv
from .base_api import BaseApi, ROUTER
from .get_todos_api import GetTodoApi
from fastapi import Path, status, HTTPException
from validations import AdminTodoModel, AdminListTodoModel


@cbv(ROUTER)
class PutTodoApi(BaseApi):

    @ROUTER.put(
        path="/edit/{todo_id}",
        status_code=status.HTTP_200_OK,
        response_model=AdminListTodoModel,
    )
    async def edit_todo(
        self,
        db: BaseApi._DB_DEPENDENCY,
        todo_request: AdminTodoModel,
        user: BaseApi._OAUTH_DEPENDENCY,
        todo_id: int = Path(gt=0),
    ):
        if not user.get("admin"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden access."
            )

        todo = db.query(Todos).filter(
            Todos.id == todo_id
        ).first()

        if todo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found :("
            )

        todo.title = todo_request.title
        todo.description = todo_request.description
        todo.priority = todo_request.priority
        todo.complete = todo_request.complete
        todo.owner_id = todo_request.owner_id

        db.add(todo)
        db.commit()

        return await GetTodoApi().get_todo_by_id(
            db=db,
            todo_id=todo_id,
            user=user
        )

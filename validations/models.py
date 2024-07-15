from pydantic import BaseModel


class ListTodoModel(BaseModel):
    id: int
    title: str
    description: str
    priority: int
    complete: bool

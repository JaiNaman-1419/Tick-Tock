from pydantic import Field, BaseModel


class AdminTodoModel(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=255)
    priority: int = Field(gt=0, lt=6)
    complete: bool
    owner_id: int = Field(gt=0)


class AdminListTodoModel(BaseModel):
    id: int
    data: AdminTodoModel

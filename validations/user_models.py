from pydantic import Field, BaseModel


class UserModel(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str = Field(min_length=8)
    admin: bool

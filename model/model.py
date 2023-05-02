from pydantic import BaseModel


class UsersModel(BaseModel):
    id: int
    phone: str
    password: str

from pydantic import BaseModel


class UsersModel(BaseModel):
    phone: str
    password: str

from pydantic import BaseModel


class Meta(BaseModel):
    code: int
    message: str


class ResponseModel(BaseModel):
    meta: Meta
    data: dict | None | list

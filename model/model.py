from pydantic import BaseModel, validator
import re


class UsersModel(BaseModel):
    id: int
    phone: str
    password: str
 
    @validator('phone')
    def phone_match(cls, phone_number):
        if re.match('010-\d{4}-\d{4}', phone_number):
            pass
        else:
            raise ValueError('올바른 핸드폰 번호가 아닙니다')

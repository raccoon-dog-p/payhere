from fastapi import APIRouter, Depends
from utils import validator_for_sign_up, encrypt_str, is_match_user
from dependencies import get_session
from db.base_class import User
from model.user_model import UsersModel
from model.main_model import ResponseModel, Meta
from sqlalchemy.orm import scoped_session
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "d4e2959b68a3d0277103c67a041e6a88a3f1644a86dccf451baad3e6956b68b4"
ALGORITHM = "HS256"


router = APIRouter(
    prefix='/users',
    tags=['users'])


@router.post('/sign_up', summary='유저 회원가입 API')
def create_users(request_model: UsersModel, db: scoped_session = Depends(get_session)):
    validation = validator_for_sign_up(request_model.phone, db, request_model.password)
    # 유효성 검사 실패
    if not validation[0]:
        code = 400
    # 유효성 검사 성공
    else:
        code = 200
        # 회원 DB 등록
        db_user = User(
            phone=request_model.phone,
            password=encrypt_str(db, request_model.password))
        db.add(db_user)
        db.commit()
    response = ResponseModel(
        meta=Meta(code=code, message=validation[1]),
        data=request_model.dict())
    return JSONResponse(status_code=code, content=response.dict())


@router.post('/login', summary='유저 로그인 API')
def login(request_model: UsersModel, db: scoped_session = Depends(get_session)):
    validation = is_match_user(request_model.phone, request_model.password, db)
    if validation[0]:
        code = 200
        data = {
            'sub': request_model.phone,
            'exp': datetime.now() + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        token_type = 'Bearer '
        response = ResponseModel(
            meta=Meta(code=code, message=validation[1]),
            data={
                'access_token': access_token,
                'token_type': token_type})
        headers = {'Authorization': token_type + access_token}
    else:
        code = 401
        response = ResponseModel(
            meta=Meta(code=code, message=validation[1]),
            data=request_model.dict())
        headers = {'Authorization': ''}
    return JSONResponse(
        status_code=code,
        content=response.dict(),
        headers=headers)


@router.get('/logout', summary='유저 로그아웃 API')
def logout():
    response = ResponseModel(meta=Meta(code=200, message='ok'))
    return JSONResponse(
        status_code=200,
        headers={'Authorization': ''},
        content=response.dict())
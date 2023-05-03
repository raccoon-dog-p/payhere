from fastapi import APIRouter
from utils import create_session


def get_session():
    session = create_session()
    try:
        yield session
    finally:
        session.close()


router = APIRouter()


@router.post('/users/sign_up', tags=['users'])
def create_users():
    pass
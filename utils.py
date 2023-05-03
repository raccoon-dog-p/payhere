from config import engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import func, select


def create_session() -> scoped_session:
    """scoped_session 생성

    Returns:
        scoped_session: _description_
    """
    session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine))
    return session


# def encrypt_str(session: scoped_session, convert_string: str) -> str:
#     query = select(session.query())

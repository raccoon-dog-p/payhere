from utils import create_session


def get_session():
    session = create_session()
    try:
        yield session
    finally:
        session.close()
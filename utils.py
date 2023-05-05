from config import engine, ENCRYPT_KEY
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import func, select
from db.base_class import User
import re


def create_session() -> scoped_session:
    """scoped_session 생성

    Returns:
        scoped_session: _description_
    """
    session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine))
    return session


def encrypt_str(session: scoped_session, origin_word: str) -> str:
    """sql 함수를 이용한 string 암호화

    Args:
        session (Session): DB session
        origin_word (str): 암호화 전 string

    Returns:
        str: 암호화 된 string
    """
    query = select(func.HEX(func.AES_ENCRYPT(origin_word, ENCRYPT_KEY)).label('encrypted_value'))
    return session.execute(query).first()[0]


def decrypt_str(session: scoped_session, origin_word: str) -> str:
    """sql 함수를 이용한 string 복호화

    Args:
        session (Session): DB session
        origin_word (str): 암호화 된 string

    Returns:
        str: 복호화 된 string
    """
    query = select(func.AES_DECRYPT(func.UNHEX(origin_word), ENCRYPT_KEY).label('encrypted_value'))
    return session.execute(query).first()[0].decode('utf-8')


def validator_for_sign_up(
        phone_number: str,
        session: scoped_session,
        password: str) -> tuple[bool, str]:
    """ 회원가입을 위한 벨리데이션 통합 함수

    Args:
        phone_number (str): user 폰 번호
        session(object): api 요청시 생성된 db session

    Returns:
        tuple[bool, str]: 성공할 시 True, 'ok' 반환, 실패시 False, error_msg 반환
    """
    is_none_validation = _is_none_id_password(phone_number, password)
    phone_match_validation = _phone_match(phone_number)
    is_id_validation = _is_exist_users(phone_number, session)
    if not is_none_validation[0]:
        return is_none_validation
    if not phone_match_validation[0]:
        return phone_match_validation
    if not is_id_validation[0]:
        return is_id_validation
    return True, 'ok'


def _phone_match(phone_number: str) -> tuple[bool, str]:
    """ 핸드폰 번호 validator

    Args:
        phone_number (str): 유저의 폰 번호

    Returns:
        tuple[bool, str]: 성공할 시 True, 'ok' 반환, 실패시 False, error_msg 반환
    """
    status = True
    msg = 'ok'
    if '-' not in phone_number:
        msg = '핸드폰 번호에는 - 가 포함되어 있어야 합니다'
        status = False
    elif not re.match('010-\d{4}-\d{4}', phone_number):
        msg = '올바른 핸드폰 번호가 아닙니다'
        status = False
    return status, msg


def _is_exist_users(phone_number: str, session: scoped_session) -> tuple[bool, str]:
    """ 이미 존재하는 유저인지 판별하는 함수

    Args:
        phone_number (str): 로그인 할 떄 사용 하는 폰번호

    Returns:
        tuple[bool, str]: 성공할 시 True, 'ok' 반환, 실패시 False, error_msg 반환
    """
    msg = 'ok'
    user_phone = session.query(User).filter(
        (User.phone == phone_number)).first()
    if user_phone:
        status = False
        msg = '이미 가입한 핸드폰 번호입니다'
    else:
        status = True
    return status, msg


def _is_none_id_password(phone_number: str, password: str) -> tuple[bool, str]:
    """ 아이디, 패스워드 빈 값 검증

    Args:
        phone_number (str): 로그인 할 때 사용하는 폰 번호
        password (str): 로그인 할 때 사용하는 패스워드

    Returns:
        tuple[bool, str]: 성공할 시 True, 'ok' 반환, 실패시 False, error_msg 반환
    """
    if phone_number == '' or password == '':
        status = False
        msg = '아이디 또는 패스워드는 빈 값일 수 없습니다.'
    else:
        status = True
        msg = ''
    return status, msg


def is_match_user(phone_number: str, password: str, session: scoped_session) -> tuple[bool, str]:
    """ 로그인 시 회원 정보 DB 비교 함수

    Args:
        phone_number (str): 유저 핸드폰 번호
        password (str): 유저 비밀번호
        session (scoped_session): db_session

    Returns:
        tuple[bool, str]: 성공할 시 True, 'ok' 반환, 실패시 False, error_msg 반환
    """
    # 유저의 핸드폰 번호로 기존 DB 조회
    user_db = session.query(User).filter(
        (User.phone == phone_number)).first()
    # 핸드폰 번호 존재 시 패스워드 확인
    if user_db:
        if password == decrypt_str(session, user_db.password):
            status = True
            msg = 'ok'
        else:
            status = False
            msg = '비밀번호가 일치하지 않습니다'
    # 핸드폰 번호 미 존재시 에러
    else:
        status = False
        msg = '존재하지 않는 핸드폰 번호입니다. 회원가입 해주세요!'
    return status, msg
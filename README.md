# payhere
def encrypt_str(session: Session, origin_word: str) -> str:
    """sql 함수를 이용한 string 암호화

    Args:
        session (Session): DB session
        origin_word (str): 암호화 전 string

    Returns:
        str: 암호화 된 string
    """
    query = select([func.HEX(func.AES_ENCRYPT(origin_word, ENCRYPT_KEY)).label('encrypted_value')])
    return session.execute(query).first()[0]

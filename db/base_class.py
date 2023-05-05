from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects import mysql

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(String(20))  # 핸드폰 번호 벨리데이터 필요
    password = Column(String(100))  # 패스워드 암호화 시킬 예정


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    category = Column(String(100), comment='상품 카테코리')
    price = Column(mysql.INTEGER(7), comment='판매 가격')
    cost = Column(mysql.INTEGER(7), comment='원가')
    product_name = Column(String(100), comment='상품 이름')
    product_detail = Column(String(500), nullable=True, comment='상품 설명')
    barcode = Column(mysql.INTEGER(13), comment='바코드')
    expiration_date = Column(DateTime(), comment='유통 기한')
    size = Column(String(10), nullable=True, comment='사이즈 small or large')

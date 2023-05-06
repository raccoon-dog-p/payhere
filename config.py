from sqlalchemy import create_engine
ENCRYPT_KEY = 'payhere'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = "d4e2959b68a3d0277103c67a041e6a88a3f1644a86dccf451baad3e6956b68b4"
ALGORITHM = "HS256"
user = "root"
pwd = "qweasd199$"
host = "localhost"
port = 3306
db_url = f'mysql+pymysql://{user}:{pwd}@{host}:{port}/payhere?charset=utf8mb4'

engine = create_engine(db_url, pool_size=5, max_overflow=5, echo=True)

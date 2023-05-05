from sqlalchemy import create_engine
ENCRYPT_KEY = 'payhere'

user = "root"
pwd = "qweasd199$"
host = "localhost"
port = 3306
db_url = f'mysql+pymysql://{user}:{pwd}@{host}:{port}/payhere'

engine = create_engine(db_url, pool_size=5, max_overflow=5, echo=True)

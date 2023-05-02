from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

user = "root"
pwd = "qweasd199$"
host = "localhost"
port = 3306
db_url = f'mysql+pymysql://{user}:{pwd}@{host}:{port}'

engine = create_engine(db_url, pool_size=5, max_overflow=5, echo=True)
session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine))

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


from sqlalchemy.orm import sessionmaker, scoped_session

DB_URI = "mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db}"
CONFIG = {
  "user": "root",
  "password": 'Ma.011235813',
  "host": '127.0.0.1',
  "port": "3306",
  "db": 'smartLol'
}
engine = create_engine(DB_URI.format(**CONFIG))
Base = declarative_base()


session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base.metadata.create_all(engine)

from database.models import Configuration
version = session.query(Configuration).filter_by(code="champion version").one().value

def init_db():
    import database.models
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    pass

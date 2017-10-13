from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


from sqlalchemy.orm import sessionmaker, scoped_session

DB_URI = "mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db}"

engine = None #create_engine(DB_URI.format(**CONFIG))
Base = declarative_base()


session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base.metadata.create_all(engine)


def init_db():
    import database.models
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    pass

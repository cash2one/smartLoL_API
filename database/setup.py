from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import json
import os.path


from sqlalchemy.orm import sessionmaker, scoped_session

DB_URI = "mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db}"
config_file = os.path.join(os.path.dirname(__file__), "db.config")
with open(config_file, "r") as infile:
    CONFIG = json.load(infile)
engine = create_engine(DB_URI.format(**CONFIG))
Base = declarative_base()

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def init_db():
    import database.models
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    init_db()

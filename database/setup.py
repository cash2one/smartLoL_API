from sqlalchemy import create_engine
import json
import os.path
from database.base import Base
from sqlalchemy.orm import sessionmaker, scoped_session


DB_URI = "mysql+mysqldb://{user}:{password}@{host}:{port}/{db}?charset=utf8"
config_file = os.path.join(os.path.dirname(__file__), "db.config")
with open(config_file, "r") as infile:
    CONFIG = json.load(infile)
engine = create_engine(DB_URI.format(**CONFIG))

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def init_db():
    import database.models
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    init_db()

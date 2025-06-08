from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine(
    "sqlite:///data/database.sqlite",
    echo=True,
)

Session = sessionmaker(engine)

class Base(DeclarativeBase):
    pass

def create_database():
    Base.metadata.create_all(engine)

def delete_database():
    Base.metadata.clear()
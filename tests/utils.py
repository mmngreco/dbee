import os
from typing import Optional, Type
from sqlalchemy.engine import Engine
from sqlmodel import Field, Session, SQLModel, create_engine


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None


def create_db(url) -> Engine:
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

    engine = create_engine(url)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.commit()

    return engine


def remove_db(name="database.db") -> bool:
    os.remove(name)
    return True


class DataBaseTest:
    def __init__(self, name="test.db") -> None:
        self.name = name
        self.url = f"sqlite:///{name}"
        self.engine = create_db(self.url)

    def __enter__(self) -> Type:
        return self.url

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        remove_db(self.name)



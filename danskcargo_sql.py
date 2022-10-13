from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from sqlalchemy import Column
from sqlalchemy import ForeignKey

from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Date

from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import delete

from datetime import date

Database = 'sqlite:///dc1.db'
Base = declarative_base()  # creating the registry and declarative base classes - combined into one step. Base will serve as the base class for the ORM mapped classes we declare.


class Container(Base):
    __tablename__ = "container"
    id = Column(Integer, primary_key=True)
    weight = Column(Integer)
    destination = Column(String)

    def __repr__(self):
        return f"Container({self.id=:4}    {self.weight=:16}    {self.destination=})"


class Aircraft(Base):
    __tablename__ = "aircraft"
    id = Column(Integer, primary_key=True)
    max_cargo_weight = Column(Integer)
    registration = Column(String)

    def __repr__(self):
        return f"Aircraft ({self.id=:4},   {self.max_cargo_weight=:6},  {self.registration=})"


class Transport(Base):
    __tablename__ = "transport"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    container_id = Column(Integer, ForeignKey("container.id"), nullable=False)
    aircraft_id = Column(Integer, ForeignKey("aircraft.id"), nullable=False)

    def __repr__(self):
        return f"Transporter({self.id=}, {self.date=}, {self.container_id=}, {self.aircraft_id=})"


def create_test_data_1():
    with Session(engine) as session:
        new_items = []
        # new_items.append(Container(weight=1200, destination="Oslo"))
        # new_items.append(Container(weight=700, destination="Helsinki"))
        # new_items.append(Container(weight=1800, destination="Helsinki"))
        # new_items.append(Container(weight=1000, destination="Helsinki"))
        # new_items.append(Aircraft(max_cargo_weight=2000, registration="OY-CBS"))
        # new_items.append(Aircraft(max_cargo_weight=3000, registration="OY-THR"))
        a_date = date(day=10, month=12, year=2022)
        new_items.append(Transport(date=a_date, container_id=2, aircraft_id=3))
        session.add_all(new_items)
        session.commit()


def select_container():  # https://docs.sqlalchemy.org/en/14/tutorial/data_select.html
    with Session(engine) as session:
        print("\nsession.scalars(select(Container).where(Container.id >= '4'))")
        containers = session.scalars(select(Container))  # very useful for converting into our data class
        result = []
        for container in containers:
            print(container)
            result.append(container)
    return result


def select_all(classparam):  # https://docs.sqlalchemy.org/en/14/tutorial/data_select.html
    with Session(engine) as session:
        records = session.scalars(select(classparam))  # very useful for converting into our data class
        result = []
        for record in records:
            # print(record)
            result.append(record)
    return result


def get_record(classparam, record_id):  # https://docs.sqlalchemy.org/en/14/tutorial/data_select.html
    with Session(engine) as session:
        record = session.scalars(select(classparam).where(classparam.id == record_id)).first()  # very useful for converting into our data class
    return record


def update_example():  # https://docs.sqlalchemy.org/en/14/tutorial/orm_data_manipulation.html#orm-enabled-update-statements
    with Session(engine) as session:
        print("\nsession.execute(update(Container).where(Container.id == 5).values(name='new name'))")
        session.execute(update(Container).where(Container.id == 5).values(name="new name"))
        # session.execute(update(Container).where(Container.id == 5).values(name="sandy"))
        print("\nsession.scalars(select(Container).where(Container.id >= '0'))")
        containers = session.scalars(select(Container).where(Container.id >= "0"))  # very useful for converting into our data class
        for container in containers:
            print(container, type(container))
        # session.commit()  # makes changes permanent in database


def update_container(container):  # https://docs.sqlalchemy.org/en/14/tutorial/orm_data_manipulation.html#orm-enabled-update-statements
    with Session(engine) as session:
        session.execute(update(Container).where(Container.id == container.id).values(weight=container.weight, destination=container.destination))
        session.commit()  # makes changes permanent in database


def create_container(container):  # https://docs.sqlalchemy.org/en/14/tutorial/orm_data_manipulation.html#orm-enabled-update-statements
    with Session(engine) as session:
        container.id = None
        session.add(container)
        session.commit()  # makes changes permanent in database


def delete_example():  # https://docs.sqlalchemy.org/en/14/tutorial/orm_data_manipulation.html#orm-enabled-delete-statements
    with Session(engine) as session:
        print("\nsession.execute(delete(Container).where(Container.id == 5))")
        session.execute(delete(Container).where(Container.id == 5))
        print("\nsession.scalars(select(Container).where(Container.id >= '0'))")
        print("\nsession.scalars(select(Container).where(Container.id >= '0'))")
        containers = session.scalars(select(Container).where(Container.id >= "0"))  # very useful for converting into our data class
        for container in containers:
            print(container, type(container))
        # session.commit()  # makes changes permanent in database


def insert_example():  # https://docs.sqlalchemy.org/en/14/tutorial/orm_data_manipulation.html#orm-enabled-delete-statements
    with Session(engine) as session:
        krabs = Container(name="ehkrabs", fullname="Eugene H. Krabs")
        squidward = Container(name="squidward", fullname="Squidward Tentacles")
        session.add(squidward)
        session.add(krabs)
        # session.flush()
        session.commit()  # makes changes permanent in database
        containers = session.scalars(select(Container).where(Container.id >= "0"))  # very useful for converting into our data class
        for container in containers:
            print(container, type(container), type(containers))


if __name__ == "__main__":
    # Executed when invoked directly
    engine = create_engine(Database, echo=False, future=True)  # https://docs.sqlalchemy.org/en/14/tutorial/engine.html   The start of any SQLAlchemy application is an object called the Engine. This object acts as a central source of connections to a particular database, providing both a factory as well as a holding space called a connection pool for these database connections. The engine is typically a global object created just once for a particular database server, and is configured using a URL string which will describe how it should connect to the database host or backend.
    Base.metadata.create_all(engine)
    # create_test_data_1()
    # select_all(Container)
    # select_all(Aircraft)
    select_all(Transport)
    print(get_record(Container, 2))
    print(get_record(Aircraft, 3))
    # update_example(engine)
    # delete_example(engine)
    # insert_example(engine)
    # select_text(engine)
else:
    # Executed when imported
    engine = create_engine(Database, echo=False, future=True)  # https://docs.sqlalchemy.org/en/14/tutorial/engine.html   The start of any SQLAlchemy application is an object called the Engine. This object acts as a central source of connections to a particular database, providing both a factory as well as a holding space called a connection pool for these database connections. The engine is typically a global object created just once for a particular database server, and is configured using a URL string which will describe how it should connect to the database host or backend.
    Base.metadata.create_all(engine)


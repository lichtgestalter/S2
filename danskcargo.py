from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Date
from sqlalchemy import text
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import delete

Database = 'sqlite:///dc1.db'
Base = declarative_base()  # creating the registry and declarative base classes - combined into one step. Base will serve as the base class for the ORM mapped classes we declare.


class Container(Base):
    __tablename__ = "container"
    id = Column(Integer, primary_key=True)
    weight = Column(Integer)
    destination = Column(String)

    def __repr__(self):
        return f"Container({self.id=}, {self.weight=}, {self.destination=})"


class Aircraft(Base):
    __tablename__ = "aircraft"
    id = Column(Integer, primary_key=True)
    max_cargo_weight = Column(Integer)
    registration = Column(String)

    def __repr__(self):
        return f"Aircraft({self.id=}, {self.max_cargo_weight=}, {self.registration=})"


class Transport(Base):
    __tablename__ = "transport"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    container_id = Column(Integer, ForeignKey("container.id"), nullable=False)
    aircraft_id = Column(Integer, ForeignKey("aircraft.id"), nullable=False)

    def __repr__(self):
        return f"Transporter({self.id=}, {self.date=}, {self.container=}, {self.aircraft=})"


def create_test_data_1(engine):
    with Session(engine) as session:
        new_items = []
        # container1 = Container(weight=1200, destination="Oslo")
        # container2 = Container(weight=700, destination="Helsinki")
        # container3 = Container(weight=1800, destination="Helsinki")
        # container4 = Container(weight=1000, destination="Helsinki")
        # aircraft1 = Aircraft(max_cargo_weight=2000, registration="OY-CBS")
        # aircraft1 = Aircraft(max_cargo_weight=3000, registration="OY-THR")
        new_items.append(Container(weight=1200, destination="Oslo"))
        new_items.append(Container(weight=700, destination="Helsinki"))
        new_items.append(Container(weight=1800, destination="Helsinki"))
        new_items.append(Container(weight=1000, destination="Helsinki"))
        new_items.append(Aircraft(max_cargo_weight=2000, registration="OY-CBS"))
        new_items.append(Aircraft(max_cargo_weight=3000, registration="OY-THR"))
        # session.add_all([container1, container2, container3, container4])
        session.add_all(new_items)
        session.commit()


def select_text(engine):  # https://docs.sqlalchemy.org/en/14/tutorial/dbapi_transactions.html
    with Session(engine) as session:
        param_dic = {"param1": -2}  # This dictionary contains the parameters which will be used in the following SQL query.
        sql_text = text("SELECT * FROM user_account WHERE id > :param1")
        result = session.execute(sql_text, param_dic)
        for row in result:
            print(row)


def select_SQL_Expression(engine):  # https://docs.sqlalchemy.org/en/14/tutorial/data_select.html
    with Session(engine) as session:
        # stmt = select(User)
        # stmt = select(User).where(User.name == "spongebob")
        print("\nfor row in session.execute(select(User).where(User.name == 'spongebob')):")
        for row in session.execute(select(User).where(User.name == "spongebob")):
            print(row, type(row))
        print("\nsession.scalars(select(User)).first()")
        user = session.scalars(select(User)).first()
        print(user, type(user))
        print("\nsession.scalars(select(User).where(User.id >= '4'))")
        users = session.scalars(select(User).where(User.id >= "4"))  # very useful for converting into our data class
        for user in users:
            print(user, type(user))
        print("\nsession.execute(select(User.name, User.fullname).where(User.id >= '4').where(User.name >= 's'))")
        users = session.execute(select(User.name, User.fullname).where(User.id >= "4").where(User.name >= "s"))
        for user in users:
            print(user, type(user))
        # print("[0]", users[0], type(users[0]))  # TypeError: 'ChunkedIteratorResult' object is not subscriptable


def update_example(engine):  # https://docs.sqlalchemy.org/en/14/tutorial/orm_data_manipulation.html#orm-enabled-update-statements
    with Session(engine) as session:
        print("\nsession.execute(update(User).where(User.id == 5).values(name='new name'))")
        session.execute(update(User).where(User.id == 5).values(name="new name"))
        # session.execute(update(User).where(User.id == 5).values(name="sandy"))
        print("\nsession.scalars(select(User).where(User.id >= '0'))")
        users = session.scalars(select(User).where(User.id >= "0"))  # very useful for converting into our data class
        for user in users:
            print(user, type(user))
        # session.commit()  # makes changes permanent in database


def delete_example(engine):  # https://docs.sqlalchemy.org/en/14/tutorial/orm_data_manipulation.html#orm-enabled-delete-statements
    with Session(engine) as session:
        print("\nsession.execute(delete(User).where(User.id == 5))")
        session.execute(delete(User).where(User.id == 5))
        print("\nsession.scalars(select(User).where(User.id >= '0'))")
        users = session.scalars(select(User).where(User.id >= "0"))  # very useful for converting into our data class
        for user in users:
            print(user, type(user))
        # session.commit()  # makes changes permanent in database


def insert_example(engine):  # https://docs.sqlalchemy.org/en/14/tutorial/orm_data_manipulation.html#orm-enabled-delete-statements
    with Session(engine) as session:
        krabs = User(name="ehkrabs", fullname="Eugene H. Krabs")
        squidward = User(name="squidward", fullname="Squidward Tentacles")
        session.add(squidward)
        session.add(krabs)
        # session.flush()
        session.commit()  # makes changes permanent in database
        users = session.scalars(select(User).where(User.id >= "-1"))  # very useful for converting into our data class
        for user in users:
            print(user, type(user))


engine = create_engine(Database, echo=True, future=True)  # https://docs.sqlalchemy.org/en/14/tutorial/engine.html   The start of any SQLAlchemy application is an object called the Engine. This object acts as a central source of connections to a particular database, providing both a factory as well as a holding space called a connection pool for these database connections. The engine is typically a global object created just once for a particular database server, and is configured using a URL string which will describe how it should connect to the database host or backend.
Base.metadata.create_all(engine)
create_test_data_1(engine)
# pandas_read_write()
# select_text(engine)
# select_SQL_Expression(engine)
# update_example(engine)
# delete_example(engine)
# insert_example(engine)
# select_text(engine)

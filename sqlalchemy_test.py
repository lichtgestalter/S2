from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Date
from sqlalchemy import text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
import pandas as pd

Base = declarative_base()  # creating the registry and declarative base classes - combined into one step. Base will serve as the base class for the ORM mapped classes we declare.


class User(Base):
    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)
    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")  # indicates to the ORM that these User and Address classes refer to each other in a one to many / many to one relationship.

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)
    user = relationship("User", back_populates="addresses")  # indicates to the ORM that these User and Address classes refer to each other in a one to many / many to one relationship.

    def __repr__(self):
        return f"Address(id={self.id}, email_address={self.email_address!r})"


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
    container = Column(Integer, ForeignKey("container.id"), nullable=False)
    aircraft = Column(Integer, ForeignKey("aircraft.id"), nullable=False)

    def __repr__(self):
        return f"Transporter({self.id=}, {self.date=}, {self.container=}, {self.aircraft=})"


def create_test_data_1(engine):
    with Session(engine) as session:
        spongebob = User(name="spongebob", fullname="Spongebob Squarepants", addresses=[Address(email_address="spongebob@sqlalchemy.org")])
        sandy = User(name="sandy", fullname="Sandy Cheeks", addresses=[Address(email_address="sandy@sqlalchemy.org"), Address(email_address="sandy@squirrelpower.org")])
        patrick = User(name="patrick", fullname="Patrick Star")
        session.add_all([spongebob, sandy, patrick])
        session.commit()
        # Simple SELECT
        stmt = (select(User)
                .where(User.name.in_(["spongebob", "sandy"])))
        for user in session.scalars(stmt):
            print("Uli1  ", user)
        # SELECT with JOIN
        stmt = (select(Address)
                .join(Address.user)
                .where(User.name == "sandy")
                .where(Address.email_address == "sandy@sqlalchemy.org"))
        sandy_address = session.scalars(stmt).one()
        print("Uli2  ", sandy_address)


def test_pandas_read_write():
    old_engine = create_engine('sqlite:///foo.db', echo=True, future=False)  # pandas not yet compatible with future==True (sqlalchemy version >= 1.4)
    Base.metadata.create_all(old_engine)
    with Session(old_engine) as session:
        df = pd.read_sql("user_account", old_engine, index_col=None, coerce_float=True, params=None, parse_dates=None, columns=None, chunksize=None)
        print(df)
        df.to_sql('user_account', old_engine, if_exists='replace', index=False)
        df = pd.read_sql("user_account", old_engine, index_col=None, coerce_float=True, params=None, parse_dates=None, columns=None, chunksize=None)
        print(df)


def execute_text_example(engine):  # https://docs.sqlalchemy.org/en/14/tutorial/dbapi_transactions.html
    with Session(engine) as session:
        param_dic = {"param1": -2}  # This dictionary contains the parameters which will be used in the following SQL query.
        sql_text = text("SELECT * FROM user_account WHERE id > :param1")
        result = session.execute(sql_text, param_dic)
        for row in result:
            print(row)


def select_SQL_Expression(engine):  # https://docs.sqlalchemy.org/en/14/tutorial/data_select.html
    with Session(engine) as session:
        stmt = select(User)
        stmt = select(User).where(User.name == "spongebob")
        print("\nfor row in session.execute(select(User).where(User.name == 'spongebob')):")
        for row in session.execute(select(User).where(User.name == "spongebob")):
            print(row, type(row))
        print("\nsession.scalars(select(User)).first()")
        user = session.scalars(select(User)).first()
        print(user, type(user))
        print("\nsession.scalars(select(User))")
        users = session.scalars(select(User))
        for user in users:
            print(user, type(user))


engine = create_engine('sqlite:///foo.db', echo=False, future=True)  # https://docs.sqlalchemy.org/en/14/tutorial/engine.html   The start of any SQLAlchemy application is an object called the Engine. This object acts as a central source of connections to a particular database, providing both a factory as well as a holding space called a connection pool for these database connections. The engine is typically a global object created just once for a particular database server, and is configured using a URL string which will describe how it should connect to the database host or backend.
Base.metadata.create_all(engine)
# create_test_data(engine)
# test_pandas_read_write()
# execute_text_example(engine)
select_SQL_Expression(engine)

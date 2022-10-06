from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
import pandas

Base = declarative_base()

#test
class User(Base):
    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)
    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)
    user = relationship("User", back_populates="addresses")

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


class Transporter(Base):
    __tablename__ = "transporter"
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
        # SELECT with JOINmodel
        stmt = (select(Address)
                .join(Address.user)
                .where(User.name == "sandy")
                .where(Address.email_address == "sandy@sqlalchemy.org"))
        sandy_address = session.scalars(stmt).one()
        print("Uli2  ", sandy_address)


# engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
engine = create_engine('sqlite:///foo.db')
Base.metadata.create_all(engine)
# create_test_data(engine)
with Session(engine) as session:
    df = pandas.read_sql("user_account", engine, index_col=None, coerce_float=True, params=None, parse_dates=None, columns=None, chunksize=None)
    print(df)
    df.to_sql('user_account', engine, if_exists='replace', index=False)
    df = pandas.read_sql("user_account", engine, index_col=None, coerce_float=True, params=None, parse_dates=None, columns=None, chunksize=None)
    print(df)
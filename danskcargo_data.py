from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, Date


Base = declarative_base()  # creating the registry and declarative base classes - combined into one step. Base will serve as the base class for the ORM mapped classes we declare.


class Container(Base):
    __tablename__ = "container"
    id = Column(Integer, primary_key=True)
    weight = Column(Integer)
    destination = Column(String)

    def __repr__(self):
        return f"Container({self.id=:4}    {self.weight=:16}    {self.destination=})"


def container2tuple(record):  # Convert Container to tuple
    return record.id, record.weight, record.destination


def tuple2container(record):  # Convert tuple to Container
    container = Container(id=record[0], weight=record[1], destination=record[2])
    return container


class Aircraft(Base):
    __tablename__ = "aircraft"
    id = Column(Integer, primary_key=True)
    max_cargo_weight = Column(Integer)
    registration = Column(String)

    def __repr__(self):
        return f"Aircraft ({self.id=:4},   {self.max_cargo_weight=:6},  {self.registration=})"


def aircraft2tuple(record):  # Convert aircraft to tuple
    return record.id, record.max_cargo_weight, record.registration


def tuple2aircraft(record):  # Convert tuple to aircraft
    aircraft = Aircraft(id=record[0], max_cargo_weight=record[1], registration=record[2])
    return aircraft


class Transport(Base):
    __tablename__ = "transport"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    container_id = Column(Integer, ForeignKey("container.id"), nullable=False)
    aircraft_id = Column(Integer, ForeignKey("aircraft.id"), nullable=False)

    def __repr__(self):
        return f"Transporter({self.id=}, {self.date=}, {self.container_id=}, {self.aircraft_id=})"


def transport2tuple(record):  # Convert transport to tuple
    return record.id, record.date, record.container_id, record.aircraft_id


def tuple2transport(record):  # Convert tuple to transport
    transport = Transport(id=record[0], date=record[1], container_id=record[2], aircraft_id=record[3])
    return transport

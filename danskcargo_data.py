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


class Transport(Base):
    __tablename__ = "transport"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    container_id = Column(Integer, ForeignKey("container.id"), nullable=False)
    aircraft_id = Column(Integer, ForeignKey("aircraft.id"), nullable=False)

    def __repr__(self):
        return f"Transporter({self.id=}, {self.date=}, {self.container_id=}, {self.aircraft_id=})"

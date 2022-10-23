from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import extract

import danskcargo_data as dcd
import danskcargo_sql as dcsql


def booked_cargo(aircraft, date_):
    #
    with Session(dcsql.engine) as session:
        records = session.scalars(select(dcd.Transport).where(dcd.Transport.aircraft_id == aircraft.id).where(extract('day', dcd.Transport.date) == date_.day).where(extract('month', dcd.Transport.date) == date_.month).where(extract('year', dcd.Transport.date) == date_.year))
        # records = session.scalars(select(dcd.Transport).where(dcd.Transport.aircraft_id == aircraft.id).where(dcd.Transport.date == date_))
        weight = 0
        for record in records:
            weight += dcsql.get_record(dcd.Container, record.container_id).weight
            print("booked cargo in kg so far: ", weight)
    print("booked cargo in kg: ", weight)
    return weight


def capacity_available(aircraft, date_, new_container):
    #
    booked = booked_cargo(aircraft, date_)
    return aircraft.max_cargo_weight >= booked + new_container.weight


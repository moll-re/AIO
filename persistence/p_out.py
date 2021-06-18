from models import db
from models import *
import datetime as dt
from random import randint


def create_tables():
    with db:
        db.create_tables([SensorMetric, ChatMetric, ErrorMetric])


create_tables()
# read from json, excel, txt ... whatever
now = dt.datetime.timestamp(dt.datetime.now())


for i in range(1000):
    with db:
        sensor_data = SensorMetric.create(
            time = now + i,
            temperature = 23,
            humidity = 30 + randint(0,20),
            luminosity = 1
        )
        chat = ChatMetric(
            time = now + i,
            activity = "Hello world"
        )
        errors = ErrorMetric(
            time = now + i,
            error = "Could not load module"
        )
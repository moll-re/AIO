from peewee import *
import datetime
import logging
logger = logging.getLogger(__name__)
from threading import Thread

from . import keys
dbk = keys.db_keys


db = MySQLDatabase(dbk["name"], user=dbk["username"], password=dbk["password"], host=dbk["url"], port=dbk["port"], autorollback=True)



class DBModel(Model):
    # specific to the above DB
    class Meta:
        database = db

    def save(self):
        # fail-safe writing of the db-object. Usually threaded because the caller is threaded
        try:
            # db.connect()
            super().save()
            # db.close()
        except Exception as e:
            logger.error("Could not write to db. Dropping content of {}".format(self.__class__.__name__))
            print(e)
            # db.atomic().rollback()


class Metric(DBModel):
    time = DateTimeField()
        



class SensorMetric(Metric):
    # this is a continuous metric
    temperature = IntegerField()
    humidity = IntegerField()
    luminosity = IntegerField()


class ChatMetric(Metric):
    read = BooleanField()
    send = BooleanField()
    execute = BooleanField()


class ErrorMetric(Metric):
    # same as above
    error = TextField()


class List(DBModel):
    name = CharField(unique=True)
    content = TextField() # unlimited length, use to serialise list into
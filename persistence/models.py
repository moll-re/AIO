from peewee import *
# from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin
import logging
logger = logging.getLogger(__name__)



db = DatabaseProxy()
# set the nature of the db at runtime

class ReconnectDataBase(ReconnectMixin, MySQLDatabase):
    pass


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
            logger.error(e)
            # db.atomic().rollback()

    # def get(self, *query, **filters):
    #     try:
    #         return super().get(*query, **filters)
    #     except Exception as e:
    #         logger.error("Error while executing get: {}".format(e))
    #         print(query, filters)


class Metric(DBModel):
    time = DateTimeField()
        

### Actual metrics:

class SensorMetric(Metric):
    # this is a continuous metric
    temperature = IntegerField()
    humidity = IntegerField()
    luminosity = IntegerField()
    default = {"temperature": 100, "humidity": 100, "luminosity": 100}



class ChatMetric(Metric):
    read = BooleanField()
    send = BooleanField()
    execute = BooleanField()
    default = {"read": False, "send": False, "execute": False}


class ErrorMetric(Metric):
    # same as above
    error = TextField()
    default = {"error": "SQL connection broke off"}


class List(DBModel):
    name = CharField(unique=True)
    content = TextField() # unlimited length, use to serialise list into
    default = {"content": "SQL connection broke off"}
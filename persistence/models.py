from datetime import datetime
from peewee import *
import logging
import json

logger = logging.getLogger(__name__)


def create_tables(db):
    db.create_tables([SensorMetric, ChatMetric, ErrorMetric, List])

db = DatabaseProxy()
# set the nature of the db at runtime


class DBModel(Model):
    # specific to the above DB
    class Meta:
        database = db

class Metric(DBModel):
    time = DateTimeField(default = datetime.now())
        


### Actual metrics:

class SensorMetric(Metric):
    # this is a continuous metric
    temperature = FloatField()
    humidity = FloatField()
    luminosity = FloatField()


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

    @property
    def content_as_list(self):
        return json.loads(self.content)
    
    def set_content(self, list_content):
        self.content = json.dumps(list_content)
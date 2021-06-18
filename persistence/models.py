from peewee import *

#db = SqliteDatabase('data.db')
db = MySQLDatabase("AIO_sensors", host="192.168.1.101", port=3306, user="pi", passwd="supersecret")
# whyyy?

class Metric(Model):
    time = DateTimeField()


    class Meta:
        database = db

class SensorMetric(Metric):
    # this is a continuous metric
    temperature = IntegerField()
    humidity = IntegerField()
    luminosity = IntegerField()


class ChatMetric(Metric):
    # this gets cumulated over one hour (or one day, or...)
    activity = CharField()


class ErrorMetric(Metric):
    # same as above
    error = CharField()


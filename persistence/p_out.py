from . import models
from peewee import *
# from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin
import inspect

from . import keys
dbk = keys.db_keys


class ReconnectDataBase(ReconnectMixin, MySQLDatabase):
    pass



class DBConnector:
    """Create a connection to a remote database and log some quantities that will be visualized otherwhere"""
    def __init__(self):
        self.db = models.db
        
        self.sensors = models.SensorMetric
        self.chats = models.ChatMetric
        self.errors = models.ErrorMetric
        self.lists = models.List

        self.create_tables()

    def create_tables(self):
        self.db.create_tables([self.sensors, self.chats, self.errors, self.lists])

    

class DataBaseConnector:
    def __init__(self) -> None:
        self.db_object = models.ReconnectDataBase(
            dbk["name"],
            user=dbk["username"],
            password=dbk["password"],
            host=dbk["url"],
            port=dbk["port"],
            autorollback=True
        )
        models.db.initialize(self.db_object)

        # self.sensors = models.SensorMetric
        # self.chats = models.ChatMetric
        # self.errors = models.ErrorMetric
        # self.lists = models.List
        ## Set as property methods instead

        self.db_object.create_tables([self.sensors, self.chats, self.errors, self.lists])
    
    @property
    def sensors(self):
        self.connect_first()
        return models.SensorMetric
    
    @property
    def chats(self):
        self.connect_first()
        return models.ChatMetric
    
    @property
    def errors(self):
        self.connect_first()
        return models.ErrorMetric

    @property
    def lists(self):
        self.connect_first()
        return models.List

    def connect_first(self):
        # if self.db_object.is_closed():
        #    self.db_object.connect()
        self.db_object.connect(reuse_if_open=True)




# def auto_reconnect(func, *args, **kwargs):
#     return func

# def classwide_decorator(decorator):
#     def decorate(cls):
#         for attr in inspect.getmembers(cls, inspect.ismethod): # there's propably a better way to do this
#             # TODO: filter init
#             print(attr)
#             if callable(getattr(cls, attr)):
#                 setattr(cls, attr, decorator(getattr(cls, attr)))
#         return cls
#     return decorate

# # apply auto_reconnect to every method so that every method first checks the db connection and reconnects if necessary
# @classwide_decorator(auto_reconnect) 
# class DataBaseConnector(ReconnectMixin, MySQLDatabase):
#     def __init__(self, *args, **kwargs):
#         super().__init__(
#             dbk["name"],
#             user=dbk["username"],
#             password=dbk["password"],
#             host=dbk["url"],
#             port=dbk["port"],
#             autorollback=True,
#             *args, **kwargs)

#         models.db.initialize(self)
#         self.sensors = models.SensorMetric
#         self.chats = models.ChatMetric
#         self.errors = models.ErrorMetric
#         self.lists = models.List

#         self.create_tables([self.sensors, self.chats, self.errors, self.lists])

#     def m1(self): pass
#     def m2(self, x): pass

from . import models
from peewee import *
from playhouse.pool import PooledMySQLDatabase


import logging
logger = logging.getLogger(__name__)


from . import keys
dbk = keys.db_keys



db_connection = PooledMySQLDatabase(
    dbk["name"],
    user=dbk["username"],
    password=dbk["password"],
    host=dbk["url"],
    port=dbk["port"],
    autorollback=True
)


def auto_connect_db(action):
    def decorated(func):
        def wrapper(*args, **kwargs):
            #before:
            db_connection.connect()
            ret = func(*args, **kwargs)
            #after:
            db_connection.close()
            # also, action is in scope now
            return ret
        
        return wrapper
    return decorated



class DatabaseUtils:
    """This object is the only database-related stuff getting exposed to the other modules. It must explicitly handle the connections!"""
    def __init__(self) -> None:
        # TODO specify arguments!
        models.db.initialize(db_connection)
        models.create_tables(db_connection)


    @auto_connect_db
    def chat_count(self, attribute):
        if attribute == "read":
            return models.ChatMetric.select().where(models.ChatMetric.read == True).count()
        elif attribute == "send":
            return models.ChatMetric.select().where(models.ChatMetric.send == True).count()
        elif attribute == "execute":
            return models.ChatMetric.select().where(models.ChatMetric.execute == True).count()
        else: # does not exist
            return -1


    def chat_log(self, **kwargs):
        models.ChatMetric(**kwargs)


    def list_get(self, list_name=""):
        if not list_name: # return all
            return models.List.select()
        else:
            return models.List.get(models.List.name == list_name)
        
    
    def list_update(self, list_name, append="", replace=[]):
        if replace:
            models.List.get(models.List.name == list_name).set_content(replace)
        elif append:
            l_obj = models.List.get(models.List.name == list_name)
            l = l_obj.content_as_list
            l.append(append)
            l_obj.set_content(l)
        else:
            logger.warning("Empty update_list() query was made. Ignoring")


    def list_delete(self, list_name):
        models.List.delete().where(self.db.lists.name == self.current_name).execute()


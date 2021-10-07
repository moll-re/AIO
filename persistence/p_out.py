from . import models


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


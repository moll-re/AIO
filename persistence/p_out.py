from . import models


class DBLogging:
    """Create a connection to a remote database and log some quantities that will be visualized otherwhere"""
    def __init__(self):
        self.db = models.db
        
        self.sensors = models.SensorMetric
        self.chats = models.ChatMetric
        self.errors = models.ErrorMetric
        self.lists = models.List

    #     self.create_tables()

    # def create_tables(self):
    #     with self.db as db:
    #         db.create_tables([self.sensors, self.chats, self.errors, self.lists])

















# writin to the db gets handled through the model directly

# create_tables()
# # read from json, excel, txt ... whatever
# now = dt.datetime.timestamp(dt.datetime.now())


# for i in range(1000):
#     with db:
#         sensor_data = SensorMetric.create(
#             time = now + i,
#             temperature = 23,
#             humidity = 30 + randint(0,20),
#             luminosity = 1
#         )
#         chat = ChatMetric(
#             time = now + i,
#             activity = "Hello world"
#         )
#         errors = ErrorMetric(
#             time = now + i,
#             error = "Could not load module"
#         )
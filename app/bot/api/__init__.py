from . import reddit
from . import weather
from . import reddit
from . import search
from . import metmuseum
import os
if os.getenv("dockerized", "") == "true":
    import sys
    sys.path.append("/keys")
    import api_keys as apikeys
else:
    from . import apikeys

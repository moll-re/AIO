import requests

import logging
logger = logging.getLogger(__name__)

class FetchUpdates:
    """Fetches updates from the main server and relays them to the clock"""

    def __init__(self, server_ip, port):
        """Both methods return a list as python-object. This should be then converted to a numpy array."""
        # self.server_ip = server_ip
        self.base_url = server_ip + ":" + port
        # self.modules gets added through the caller
        self.update_calls = 0
        self.last_fetch = {}


    def start(self):
        # dummy for errorless launching
        pass
    

    def get_updates(self):
        update_url = "http://" + self.base_url + "/getupdates"
        result = self.call_api(update_url)

        return result


    def get_last(self):
        update_url = "http://" + self.base_url + "/getlast"
        result = self.call_api(update_url)

        return result
    

    def fetch_data(self):
        try:
            if self.update_calls == 0:
                fetch = self.get_last()   
            else:
                fetch = self.get_updates()
                if not fetch["is_new"]:
                    fetch = self.last_fetch
                else:
                    self.last_fetch = fetch
            
            data = fetch["data"]
            has_queue = fetch["has_queue"]
        except:
            data = {}
            has_queue = False
            
        self.update_calls += 1

        return has_queue, data



    def call_api(self, url):
        ret = {}
        try:
            result = requests.get(url)
            result = result.json()

            if result.pop("status") == "ok":
                ret = result
        except:
            logger.error("Bad api call for method {}.".format(url[url.rfind("/"):]))

        return ret

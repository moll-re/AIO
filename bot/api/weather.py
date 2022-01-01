import requests
import datetime

import logging
logger = logging.getLogger(__name__)
class WeatherFetch():
    def __init__(self, key):
        self.last_fetch = datetime.datetime.fromtimestamp(0)
        self.last_weather = ""
        self.calls = 0

        self.url = "https://api.openweathermap.org/data/2.5/onecall?"
        self.key = key

    def show_weather(self, location):
        delta = datetime.datetime.now() - self.last_fetch
        if delta.total_seconds()/60 > 60 or "\n" not in self.last_weather: # 1 hour passed:

            
            data = {"lat" : location[0], "lon" : location[1], "exclude" : "minutely,hourly", "appid" : self.key, "units" : "metric"}
            self.calls += 1
            logger.info("Just fetched weather. ({}th time)".format(self.calls))

            try:
                weather = requests.get(self.url,params=data).json()
                now = weather["current"]
                ret_weather = []
                ret_weather.append({
                    "short" : now["weather"][0]["main"],
                    "temps" : [int(now["temp"])]
                    })
                weather_days = weather["daily"]
                for i, day in enumerate(weather_days):
                    ret_weather.append({
                        "short" : day["weather"][0]["main"],
                        "temps" : [int(day["temp"]["min"]),int(day["temp"]["max"])]
                        })
            except:
                ret_weather = []

            self.last_weather = ret_weather
            self.last_fetch = datetime.datetime.now()
        else:
            ret_weather = self.last_weather

        return ret_weather

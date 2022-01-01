import requests
import datetime

import logging
logger = logging.getLogger(__name__)
class WeatherFetch():
    def __init__(self, key):
        self.last_fetch = datetime.datetime.fromtimestamp(0)
        self.last_fetch_location = []
        self.last_weather = []
        self.calls = 0

        self.url = "https://api.openweathermap.org/data/2.5/onecall?"
        self.key = key

    def show_weather(self, location):
        delta = datetime.datetime.now() - self.last_fetch
         # 1 hour passed, error, or location change
        if delta.total_seconds() > 3600 \
            or len(self.last_weather) == 0\
            or self.last_fetch_location != location:
            
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
            
                self.last_fetch_location = location
                self.last_weather = ret_weather
                self.last_fetch = datetime.datetime.now()
            except:
                ret_weather = []
        else:
            ret_weather = self.last_weather

        return ret_weather

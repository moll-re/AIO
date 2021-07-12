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
            # today = datetime.datetime.today().weekday()
            # days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

            try:
                weather = requests.get(self.url,params=data).json()
                # categories = {"Clouds": ":cloud:", "Rain": ":cloud_with_rain:", "Thunderstorm": "thunder_cloud_rain", "Drizzle": ":droplet:", "Snow": ":cloud_snow:", "Clear": ":sun:", "Mist": "Mist", "Smoke": "Smoke", "Haze": "Haze", "Dust": "Dust", "Fog": "Fog", "Sand": "Sand", "Dust": "Dust", "Ash": "Ash", "Squall": "Squall", "Tornado": "Tornado",}
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

            
            #     now = weather["current"]
            #     message = "<b>Now:</b> " + categories[now["weather"][0]["main"]] + "\n"
            #     message += ":thermometer: " + str(int(now["temp"])) + "°\n\n"

            #     weather_days = weather["daily"]
                
            #     for i, day in enumerate(weather_days):
            #         if i == 0:
            #             message += "<b>" + "Today" + ":</b> " + categories[day["weather"][0]["main"]] + "\n"
            #         else:
            #             message += "<b>" + days[(today + i + 1) % 7] + ":</b> " + categories[day["weather"][0]["main"]] + "\n"
            #         message += ":thermometer: :fast_down_button: " + str(int(day["temp"]["min"])) + "° , :thermometer: :fast_up_button: " + str(int(day["temp"]["max"])) + "°\n\n"
            # except:
            #     message = "Query failed, it's my fault, I'm sorry :sad:"
            
            self.last_weather = ret_weather
            self.last_fetch = datetime.datetime.now()
        else:
            ret_weather = self.last_weather

        return ret_weather

    # def get_weather_by_city(self, city):
    #     loc = get_coords_from_city(self, city)
    #     weather = self.show_weather(loc)
    #     return weather
        
        
    # def get_coords_from_city(self, city):
    #     url = "https://devru-latitude-longitude-find-v1.p.rapidapi.com/latlon.php"
    #     data = {"location": city}
    #     headers = {
    #         "x-rapidapi-key" : "d4e0ab7ab3mshd5dde5a282649e0p11fd98jsnc93afd98e3aa",
    #         "x-rapidapi-host" : "devru-latitude-longitude-find-v1.p.rapidapi.com",
    #     }

    #     #try:
    #     resp = requests.request("GET", url, headers=headers, params=data)
    #     result = resp.text
    #     #except:
    #     #    result = "???"
    #     return result


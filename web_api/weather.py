import requests
import api.keys
import datetime

def show_weather(location):
    url = "https://api.openweathermap.org/data/2.5/onecall?"
    data = {"lat" : location[0], "lon" : location[1], "exclude" : "minutely,hourly", "appid" : api.keys.weather_api, "units" : "metric"}
    today = datetime.datetime.today().weekday()
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    try:
        weather = requests.get(url,params=data).json()
    except:
        return "Query failed, it's my fault, I'm sorry :sad:"


    categories = {"Clouds": ":cloud:", "Rain": ":cloud_with_rain:", "Thunderstorm": "thunder_cloud_rain", "Drizzle": ":droplet:", "Snow": ":cloud_snow:", "Clear": ":sun:", "Mist": "Mist", "Smoke": "Smoke", "Haze": "Haze", "Dust": "Dust", "Fog": "Fog", "Sand": "Sand", "Dust": "Dust", "Ash": "Ash", "Squall": "Squall", "Tornado": "Tornado",}

    now = weather["current"]
    message = "<b>Today:</b> " + categories[now["weather"][0]["main"]] + "\n"
    message += ":thermometer: " + str(int(now["temp"])) + "°\n\n"

    for i, day in enumerate(weather["daily"]):

        message += "<b>" + days[(today + i + 1) % 7] + ":</b> " + categories[day["weather"][0]["main"]] + "\n"
        message += ":thermometer: :fast_down_button: " + str(int(day["temp"]["min"])) + "° , :thermometer: :fast_up_button: " + str(int(day["temp"]["max"])) + "°\n\n"

    return message

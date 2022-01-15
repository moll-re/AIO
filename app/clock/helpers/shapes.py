import numpy as np

digits = {
    "1" : np.array([
        [0,0,1],
        [0,0,1],
        [0,0,1],
        [0,0,1],
        [0,0,1]]),
    "2" : np.array([
        [1,1,1],
        [0,0,1],
        [1,1,1],
        [1,0,0],
        [1,1,1]]),
    "3" : np.array([
        [1,1,1],
        [0,0,1],
        [1,1,1],
        [0,0,1],
        [1,1,1]]),
    "4" : np.array([
        [1,0,1],
        [1,0,1],
        [1,1,1],
        [0,0,1],
        [0,0,1]]),
    "5" : np.array([
        [1,1,1],
        [1,0,0],
        [1,1,1],
        [0,0,1],
        [1,1,1]]),
    "6" : np.array([
        [1,1,1],
        [1,0,0],
        [1,1,1],
        [1,0,1],
        [1,1,1]]),
    "7" : np.array([
        [1,1,1],
        [0,0,1],
        [0,0,1],
        [0,0,1],
        [0,0,1]]),
    "8" : np.array([
        [1,1,1],
        [1,0,1],
        [1,1,1],
        [1,0,1],
        [1,1,1]]),
    "9" : np.array([
        [1,1,1],
        [1,0,1],
        [1,1,1],
        [0,0,1],
        [1,1,1]]),
    "0" : np.array([
        [1,1,1],
        [1,0,1],
        [1,0,1],
        [1,0,1],
        [1,1,1]]),
    "-" : np.array([
        [0,0,0],
        [0,0,0],
        [1,1,1],
        [0,0,0],
        [0,0,0]]),
    "-1" : np.array([
        [0,0,1],
        [0,0,1],
        [1,1,1],
        [0,0,1],
        [0,0,1]]),
    "error" : np.array([
        [1,0,1],
        [1,0,1],
        [0,1,0],
        [1,0,1],
        [1,0,1]]),
}


weather_categories = {
    "Clouds": "cloud",
    "Rain": "rain and cloud",
    "Thunderstorm": "thunder and cloud",
    "Drizzle": "rain and cloud",
    "Snow": "snow and cloud",
    "Clear": "sun",
    "Mist": "fog and clouds",
    "Smoke": "Smoke",
    "Haze": "Haze",
    "Dust": "Dust",
    "Fog": "fog",
    "Sand": "Sand",
    "Dust": "Dust",
    "Ash": "Ash",
    "Squal": "Squal",
    "Tornado": "Tornado",
    "error" : "moon"
}
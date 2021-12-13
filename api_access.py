import requests
import json

KEY = "29c2eee5f4e55470e8864ec4b405c4d6"


def getWeatherInfos(lat=43.5571085, lon=1.4684552):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={KEY}"
    response = requests.get(url=url)
    return json.loads(response.text)







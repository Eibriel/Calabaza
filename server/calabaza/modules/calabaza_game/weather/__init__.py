import requests
import json

from calabaza.modules.mongoKit import *

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

class weather():
    light_rain = [200, 201, 210, 230, 300, 310, 500, 520]
    medium_rain = [202, 211, 221, 231, 301, 501, 502, 511, 521]
    heavy_rain = [212, 232, 221, 302, 312, 313, 314, 321, 522, 531]
    very_heavy_rain = [503, 504]

    light_snow = [600, 611, 615]
    medium_snow = [612, 616, 620]
    heavy_snow = [602, 621, 622]

    CLEAR = -1
    LIGHT_RAIN = 0
    MEDIUM_RAIN = 1
    HEAVY_RAIN = 2
    VERY_HEAVY_RAIN = 3
    LIGHT_SNOW = 4
    MEDIUM_SNOW = 5
    HEAVY_SNOW = 6

    city_id = None
    latitude = None
    longitude = None
    weather_id = None
    temperature = None
    wind_speed = None
    clouds = None

    def code_to_water(self, code):
        if code in self.light_rain:
            return 0.002
        elif code in self.medium_rain:
            return 0.005
        elif code in self.heavy_rain:
            return 0.01
        elif code in self.very_heavy_rain:
            return 0.015

        return 0

    def code_to_atmosphere(self, code):
        if code in self.light_rain:
            return self.LIGHT_RAIN
        elif code in self.medium_rain:
            return self.MEDIUM_RAIN
        elif code in self.heavy_rain:
            return self.HEAVY_RAIN
        elif code in self.very_heavy_rain:
            return self.VERY_HEAVY_RAIN
        elif code in self.light_snow:
            return self.LIGHT_SNOW
        elif code in self.medium_snow:
            return self.MEDIUM_SNOW
        elif code in self.heavy_snow:
            return self.HEAVY_SNOW

        return self.CLEAR

    def check_weather(self):
        self.city_id = 2759794
        url = "http://api.openweathermap.org/data/2.5/weather?id={0}".format(
            self.city_id
        )
        r = requests.get(url, timeout=1)
        if not r:
            return
        response = json.loads(r.text)
        # print (response)

        self.city_id = response['id']
        self.latitude = response['coord']['lat']
        self.longitude = response['coord']['lon']
        self.weather_id = response['weather'][0]['id']
        self.temperature = response['main']['temp'] - 273.15
        self.wind_speed = response['wind']['speed']
        self.clouds = response['clouds']['all']

    def get(self):
        data = {
            'city_id': self.city_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'weather_id': self.weather_id,
            'temperature': self.temperature,
            'wind_speed': self.wind_speed,
            'clouds': self.clouds
        }
        return data

    def tick(self, calabaza):
        return

    def save(self):
        client = MongoClient()
        db = client.calabaza
        db.weather.create_index("city_id", name="unique_city", unique=True)

        data = db.weather.find_one({"city_id":self.city_id})

        newdata = weatherModel()
        newdata['city_id'] = self.city_id
        newdata['latitude'] =self.latitude
        newdata['longitude'] = self.longitude
        newdata['weather_id'] = self.weather_id
        newdata['temperature'] = self.temperature
        newdata['wind_speed'] = self.wind_speed
        newdata['clouds'] = self.clouds

        if data:
            key = {"city_id":self.city_id}
            db.weather.update(key, {'$set':newdata.safe()})



def min_max_val(min_, max_):
    def validate(value):
        return value >= -min_ and value <= max_
    return validate

def any_val():
    def validate(value):
        return True
    return validate

class weatherModel(Document):
    structure = {
        'city_id': int,
        'latitude': float,
        'longitude': float,
        'weather_id': int,
        'temperature': float,
        'wind_speed': float,
        'clouds': float
    }

    validators = {
        'city_id': any_val(),
        'latitude': min_max_val(-90.0, 90.0),
        'longitude': min_max_val(-90.0, 90.0),
        'weather_id': any_val(),
        'temperature': min_max_val(-100.0, 100.0),
        'wind_speed': any_val(),
        'clouds': min_max_val(0, 100)
    }

    use_dot_notation = True

    def __repr__(self):
        return "<Weather {0}".format(self.city_id)

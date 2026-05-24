import requests
from babel import Locale
import os
from dotenv import load_dotenv

load_dotenv()

API = os.getenv("WEATHER_API_KEY")
GEO_url = "http://api.openweathermap.org/geo/1.0/direct"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


class WeatherClient:
    def __init__(
        self, city_name, country_name, api=API, geo_url=GEO_url, weather_url=WEATHER_URL
    ):
        self.api = api
        self.city_name = city_name
        self.country_name = country_name
        self.geo_url = geo_url
        self.weather_url = weather_url

    def get_country_code(self):
        locale = Locale("ru")
        for code, name in locale.territories.items():
            if name.lower() == self.country_name.lower():
                country_code = code
                return country_code
        return None

    def get_coordinates(self):
        country_code = self.get_country_code()
        if not country_code:
            return None, "Код страны не найден."
        prompt = {"q": f"{self.city_name},{country_code}",
                  "limit": 1, "appid": self.api}
        response = requests.get(self.geo_url, params=prompt)
        data = response.json()
        if not data:
            return None, "Город не найден."
        lat = data[0].get("lat")
        lon = data[0].get("lon")
        return (lat, lon), None

    def get_weather_data(self):
        coordinates, error = self.get_coordinates()
        if error:
            return {"Ошибка": error}
        lat, lon = coordinates
        prompt = {
            "lat": f"{lat}",
            "lon": f"{lon}",
            "appid": f"{self.api}",
            "units": "metric",
            "lang": "ru",
        }
        response = requests.get(self.weather_url, params=prompt)
        data = response.json()
        weather_info = {
            "city_name": self.city_name,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
        }
        return weather_info

    def weather_report(self):
        weather_info = self.get_weather_data()
        if "Ошибка" in weather_info:
            print(f"Что-то пошло не так: {weather_info['Ошибка']}")
            return
        print("-" * 30)
        print(f"Город: {weather_info['city_name']}")
        print(f"Температура: {weather_info['temperature']}°C")
        print(f"Влажность: {weather_info['humidity']}%")
        print(f"Давление: {weather_info['pressure']} гПа")


if __name__ == "__main__":
    city = WeatherClient("Нью Йорк", "Соединенные Штаты")
    city.weather_report()

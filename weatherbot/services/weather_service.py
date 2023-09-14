from aiohttp.client import ClientSession
from functools import lru_cache


class WeatherService:
    def __init__(self, api_url: str, token: str, session: ClientSession):
        self.api_url = api_url
        self.token = token
        self.session = session

    @lru_cache()
    async def get_coordinates(self, city: str, country_code: str) -> tuple | None:
        async with self.session.get(
            f"{self.api_url}/geo/1.0/\
direct?q={city},{country_code}&appid={self.token}"
        ) as connection:
            if connection.status == 200:
                data: dict = await connection.json()
                if data:
                    connection.close()
                    return data[0]["lat"], data[0]["lon"]
                connection.close()
                return

    @lru_cache()
    async def get_weather(self, lat: float, lon: float):
        async with self.session.get(
            f"{self.api_url}/data/2.5/weather?\
lat={lat}&lon={lon}&appid={self.token}"
        ) as connection:
            data: dict = await connection.json()
            if data.get("sys"):
                description: str = data["weather"][0]["description"]
                icon: str = data["weather"][0]["icon"]
                temp: int = int(data["main"]["temp"] - 273.15)
                feels_like: int = int(data["main"]["feels_like"] - 273.15)
                humidity: int = data["main"]["humidity"]
                wind_speed: int = data["wind"]["speed"]
                connection.close()
                return {
                    "description": description,
                    "icon": icon,
                    "temp": temp,
                    "feels_like": feels_like,
                    "humidity": humidity,
                    "wind_speed": wind_speed
                }
            connection.close()
            return

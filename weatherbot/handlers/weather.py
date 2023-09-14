import pycountry

from envparse import env
from aiogram import Router
from aiogram.types import Message, ErrorEvent
from aiogram.filters import Command
from aiohttp.client import ClientSession

from services.weather_service import WeatherService

weather_router = Router()


@weather_router.message(Command("start"))
async def start(msg: Message):
    await msg.answer("Hey there!\nJust send me a City and Country name.\
                     \nExample: Kyiv, Ukraine")


@weather_router.message()
async def weather(msg: Message):
    weather_service = WeatherService(
        api_url=env.str("API_URL"),
        token=env.str("OPEN_WEATHER_TOKEN"),
        session=ClientSession()
    )
    city, country = msg.text.split(",")
    country_code: str = pycountry.countries.search_fuzzy(country)[0].alpha_2
    lat, lon = await weather_service.get_coordinates(
        city=city.strip(),
        country_code=country_code
    )
    weather = await weather_service.get_weather(
        lat=lat,
        lon=lon
    )
    description = weather["description"]
    icon = weather["icon"]
    temp = weather["temp"]
    feels_like = weather["feels_like"]
    wind_speed = weather["wind_speed"]
    await msg.reply(
        f"📡 Weather forecast for {city}, {country}\n\n"
        f"🌡 Temperature: {temp}°C (feels {feels_like}°C)\n\n"
        f"☁️ {description}\n"
        f"🎐 wind: {wind_speed} km/h"
        f"<a href=\"https://openweathermap.org/img/wn/{icon}@4x.png\">⁣⁣</a>",
        parse_mode="HTML"
    )
    await weather_service.session.close()


@weather_router.error()
async def error(event: ErrorEvent, *a, **k):
    await event.update.message.answer(f"Error: {event.exception}")

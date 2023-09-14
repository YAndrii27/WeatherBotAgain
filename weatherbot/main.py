from aiogram import Bot, Dispatcher
from envparse import env
import asyncio
import logging

from handlers.weather import weather_router

logger = logging.basicConfig(level="INFO")


async def main():
    env.read_envfile()
    bot = Bot(token=env.str("TELEGRAM_BOT_TOKEN"))
    dp = Dispatcher()
    dp.include_router(weather_router)
    await dp.start_polling(bot)

asyncio.run(main())

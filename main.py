import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage

from config import TELEGRAM_TOKEN
from handlers import common_router, file_router

logging.basicConfig(level=logging.INFO)

router = Router()


async def main():
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(common_router, file_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

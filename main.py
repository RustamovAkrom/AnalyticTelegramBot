import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from src.config import settings
from src.handlers import router

bot = Bot(token=settings.TELEGRAM_TOKEN)
dp = Dispatcher()


dp.include_router(router)


async def main() -> None:
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        pass


if __name__=='__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

import sys
import asyncio
import logging

from aiogram import Bot, Dispatcher
from t0d0d0d0.core.config import bot_token
from t0d0d0d0.bot.handlers.auth import router as messageRouter


dp = Dispatcher()


dp.include_router(messageRouter)

async def main() -> None:
    global bot
    bot = Bot(bot_token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
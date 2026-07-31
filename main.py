import asyncio
import logging

from aiogram import Dispatcher

from app.bot import bot
from app.database import initialize_database
from app.handlers import routers
from app.middlewares.logging import LoggingMiddleware
from app.scheduler.scheduler import start_scheduler


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

# Убираем лишний шум
logging.getLogger("apscheduler").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)


dp = Dispatcher()

# Подключаем middleware для логирования
dp.message.middleware(LoggingMiddleware())
dp.callback_query.middleware(LoggingMiddleware())


async def main():

    # Инициализация базы
    initialize_database()

    # Подключаем роутеры
    for router in routers:
        dp.include_router(router)

    # Запуск планировщика
    start_scheduler()

    logging.info("BOT STARTED")

    # Запуск бота
    await dp.start_polling(bot)


if __name__ == "__main__":

    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        logging.info("BOT STOPPED")
import asyncio
import logging

from app.bot import bot
from app.database import initialize_database
from app.dispatcher import BanderaDispatcher
from app.handlers import routers
from app.middlewares.logging import LoggingMiddleware
from app.scheduler.scheduler import scheduler, start_scheduler


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

# Убираем лишний шум
logging.getLogger("apscheduler").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)


dp = BanderaDispatcher()

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
    try:
        await dp.start_polling(bot)
    finally:
        if scheduler.running:
            scheduler.shutdown(wait=False)


if __name__ == "__main__":

    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        logging.info("BOT STOPPED")
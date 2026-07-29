import asyncio
import logging

from aiogram import Dispatcher

from app.bot import bot
from app.database import initialize_database
from app.handlers import routers

from app.scheduler.scheduler import start_scheduler



logging.basicConfig(
    level=logging.INFO
)



dp = Dispatcher()



async def main():

    # Инициализация базы
    initialize_database()


    # Подключаем роутеры
    for router in routers:
        dp.include_router(router)


    # Запуск планировщика
    start_scheduler()


    print("BOT STARTED")


    await dp.start_polling(
        bot
    )



if __name__ == "__main__":

    try:
        asyncio.run(
            main()
        )

    except KeyboardInterrupt:

        print(
            "BOT STOPPED"
        )
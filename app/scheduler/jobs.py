from datetime import datetime

from app.bot import bot
from app.database.repository import SettingsRepository


last_sent = None



async def check_prime():

    global last_sent


    settings = SettingsRepository.get_settings()


    if not settings:
        return


    # Напоминания выключены
    if not settings["reminders_enabled"]:
        return


    # Нет группы
    if not settings["group_chat_id"]:
        return


    now = datetime.now()


    # Python weekday:
    # Monday = 0
    # Sunday = 6
    day = now.weekday() + 1


    current_time = now.strftime("%H:%M")


    prime = SettingsRepository.get_today_prime(
        day
    )


    if not prime:
        return


    # Проверяем время начала прайма
    if current_time != prime["start_time"]:
        return



    unique_key = (
        now.date(),
        prime["start_time"]
    )


    if last_sent == unique_key:
        return



    message = f"""
🇺🇦 <b>ПРАЙМ 🇺🇦</b>

🕗 Час:
{prime["start_time"]} - {prime["end_time"]}

Час заходити в гру!
Всім бути онлайн! 🔥
"""


    await bot.send_message(
        settings["group_chat_id"],
        message,
        parse_mode="HTML"
    )


    last_sent = unique_key
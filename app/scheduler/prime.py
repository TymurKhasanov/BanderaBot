from datetime import datetime

from app.bot import bot
from app.database.repository import SettingsRepository


last_sent_date = None


async def check_prime():
    global last_sent_date

    settings = SettingsRepository.get_settings()

    if not settings:
        return

    # Напоминания выключены
    if not settings["reminders_enabled"]:
        return

    # Группа не привязана
    if not settings["group_chat_id"]:
        return

    # Время прайма не задано
    if not settings["prime_time"]:
        return

    now = datetime.now()

    current_time = now.strftime("%H:%M")

    # Еще не время прайма
    if current_time != settings["prime_time"]:
        return

    today = now.strftime("%Y-%m-%d")

    # Уже отправляли сегодня
    if last_sent_date == today:
        return

    message = f"""
🇺🇦 ПРАЙМ 🇺🇦

🕗 {settings["prime_time"]}

Час заходити в гру!
Всім бути онлайн! 🔥
"""

    await bot.send_message(
        settings["group_chat_id"],
        message
    )

    last_sent_date = today
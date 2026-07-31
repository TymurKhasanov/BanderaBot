from datetime import datetime

from app.bot import bot
from app.database.repository import SettingsRepository


last_sent = None


async def check_prime():

    global last_sent

    settings = SettingsRepository.get_settings()

    if not settings:
        print("Settings not found")
        return

    # Напоминания выключены
    if not settings["reminders_enabled"]:
        print("Reminders disabled")
        return

    # Нет группы
    if not settings["group_chat_id"]:
        print("Group chat ID not configured")
        return

    now = datetime.now()

    # Monday = 0 ... Sunday = 6
    day = now.weekday() + 1

    current_time = now.strftime("%H:%M")

    prime = SettingsRepository.get_today_prime(day)

    print("=" * 50)
    print(f"NOW: {now}")
    print(f"DAY: {day}")
    print(f"CURRENT TIME: {current_time}")
    print(f"PRIME: {prime}")

    if not prime:
        print("No prime for today")
        return

    print(f"START: {prime['start_time']}")
    print(f"END: {prime['end_time']}")

    # Проверяем время начала прайма
    if current_time != prime["start_time"]:
        print("Not time yet")
        return

    unique_key = (
        now.date(),
        prime["start_time"]
    )

    if last_sent == unique_key:
        print("Already sent today")
        return

    message = f"""
🇺🇦 <b>ПРАЙМ 🇺🇦</b>

🕗 Час:
{prime["start_time"]} - {prime["end_time"]}

Час заходити в гру!
Всім бути онлайн! 🔥
"""

    print(">>> SENDING MESSAGE <<<")

    await bot.send_message(
        settings["group_chat_id"],
        message,
        parse_mode="HTML"
    )

    last_sent = unique_key
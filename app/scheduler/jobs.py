from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app.bot import bot
from app.database.repository import SettingsRepository


KYIV_TZ = ZoneInfo("Europe/Kyiv")

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

    now = datetime.now(KYIV_TZ)

    # Monday = 0 ... Sunday = 6
    day = now.weekday() + 1

    prime = SettingsRepository.get_today_prime(day)

    print("=" * 50)
    print(f"NOW: {now}")
    print(f"DAY: {day}")
    print(f"PRIME: {prime}")

    if not prime:
        print("No prime for today")
        return

    start_time = datetime.strptime(
        prime["start_time"],
        "%H:%M"
    ).time()

    notification_time = (
        datetime.combine(now.date(), start_time)
        - timedelta(minutes=30)
    ).time()

    current_time = now.time().replace(
        second=0,
        microsecond=0
    )

    print(f"START: {start_time}")
    print(f"NOTIFICATION: {notification_time}")
    print(f"CURRENT: {current_time}")
    print(f"END: {prime['end_time']}")

    if current_time != notification_time:
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

⏰ До початку прайму залишилося 30 хвилин!

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
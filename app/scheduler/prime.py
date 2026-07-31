from datetime import datetime

from app.bot import bot
from app.database.repository import SettingsRepository

last_sent = None


async def check_prime():

    global last_sent

    settings = SettingsRepository.get_settings()

    if not settings:
        print("[PRIME] Settings not found")
        return

    # Напоминания выключены
    if not settings["reminders_enabled"]:
        print("[PRIME] Reminders disabled")
        return

    # Нет группы
    if not settings["group_chat_id"]:
        print("[PRIME] Group chat ID not configured")
        return

    now = datetime.now()

    # Monday = 0 ... Sunday = 6
    day = now.weekday() + 1

    current_time = now.strftime("%H:%M")

    prime = SettingsRepository.get_today_prime(day)

    print("=" * 60)
    print(f"NOW        : {now}")
    print(f"DAY        : {day}")
    print(f"TIME       : {current_time}")
    print(f"PRIME DATA : {prime}")

    if not prime:
        print("[PRIME] No prime configured for today")
        return

    start_time = prime["start_time"]
    end_time = prime["end_time"]

    print(f"START TIME : {start_time}")
    print(f"END TIME   : {end_time}")
    print(f"EQUAL      : {current_time == start_time}")

    # Проверяем время начала прайма
    if current_time != start_time:
        print("[PRIME] Not time yet")
        return

    unique_key = (
        now.date(),
        start_time
    )

    print(f"UNIQUE KEY : {unique_key}")
    print(f"LAST SENT  : {last_sent}")

    if last_sent == unique_key:
        print("[PRIME] Already sent today")
        return

    message = f"""
🇺🇦 <b>ПРАЙМ 🇺🇦</b>

🕗 Час:
{start_time} - {end_time}

Час заходити в гру!
Всім бути онлайн! 🔥
"""

    print("[PRIME] >>> SENDING MESSAGE <<<")

    await bot.send_message(
        chat_id=settings["group_chat_id"],
        text=message,
        parse_mode="HTML"
    )

    last_sent = unique_key

    print("[PRIME] Message sent successfully")
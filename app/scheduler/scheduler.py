from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app.scheduler.jobs import check_prime
from app.database.repository import SettingsRepository


scheduler = AsyncIOScheduler()

KYIV_TZ = ZoneInfo("Europe/Kyiv")


def get_next_prime():

    now = datetime.now(KYIV_TZ)

    # Ищем ближайшее уведомление на следующие 7 дней
    for i in range(8):

        check_date = now + timedelta(days=i)

        day = check_date.weekday() + 1

        prime = SettingsRepository.get_today_prime(day)

        if not prime:
            continue

        start_time = datetime.strptime(
            prime["start_time"],
            "%H:%M"
        ).time()

        notification_datetime = (
            datetime.combine(
                check_date.date(),
                start_time,
                tzinfo=KYIV_TZ,
            )
            - timedelta(minutes=30)
        )

        # Если время уведомления уже прошло — ищем следующий прайм
        if notification_datetime <= now:
            continue

        return notification_datetime, prime

    return None, None


def start_scheduler():

    scheduler.add_job(
        check_prime,
        "interval",
        minutes=1,
    )

    scheduler.start()

    print("SCHEDULER STARTED")
    print(f"CURRENT TIME: {datetime.now(KYIV_TZ)}")

    next_time, prime = get_next_prime()

    if next_time:

        print(
            f"NEXT PRIME NOTIFICATION: "
            f"{next_time.strftime('%Y-%m-%d %H:%M')}"
        )

        print(
            f"PRIME TIME: "
            f"{prime['start_time']} - {prime['end_time']}"
        )

        print("NOTIFICATION: 30 minutes before prime")

    else:

        print("NEXT PRIME NOTIFICATION: NOT FOUND")
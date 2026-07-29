from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

from app.scheduler.jobs import check_prime
from app.database.repository import SettingsRepository


scheduler = AsyncIOScheduler()



def get_next_prime():

    now = datetime.now()


    # ищем ближайший прайм на следующие 7 дней
    for i in range(8):

        check_date = now + timedelta(days=i)

        day = check_date.weekday() + 1


        prime = SettingsRepository.get_today_prime(
            day
        )


        if not prime:
            continue


        prime_datetime = check_date.replace(
            hour=int(prime["start_time"].split(":")[0]),
            minute=int(prime["start_time"].split(":")[1]),
            second=0,
            microsecond=0
        )


        # если сегодня время уже прошло
        if prime_datetime <= now:
            continue


        return prime_datetime, prime



    return None, None



def start_scheduler():

    scheduler.add_job(
        check_prime,
        "interval",
        minutes=1
    )


    scheduler.start()


    print("SCHEDULER STARTED")


    next_time, prime = get_next_prime()


    if next_time:

        print(
            f"NEXT PRIME NOTIFICATION: "
            f"{next_time.strftime('%Y-%m-%d %H:%M')}"
        )

        print(
            f"TIME: "
            f"{prime['start_time']} - {prime['end_time']}"
        )

    else:

        print(
            "NEXT PRIME NOTIFICATION: NOT FOUND"
        )
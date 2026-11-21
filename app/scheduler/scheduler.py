import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.database.repository import SettingsRepository
from app.scheduler.jobs import check_prime


KYIV_TZ = ZoneInfo("Europe/Kyiv")
scheduler = AsyncIOScheduler(timezone=KYIV_TZ)
logger = logging.getLogger("banderabot")


def get_next_prime() -> tuple[datetime | None, object | None]:
    now = datetime.now(KYIV_TZ)
    for offset in range(8):
        check_date = now + timedelta(days=offset)
        prime = SettingsRepository.get_today_prime(check_date.weekday() + 1)
        if not prime:
            continue
        try:
            start_time = datetime.strptime(prime["start_time"], "%H:%M").time()
        except (TypeError, ValueError):
            logger.exception("Invalid prime start time in database")
            continue
        notification = (
            datetime.combine(check_date.date(), start_time, tzinfo=KYIV_TZ)
            - timedelta(minutes=30)
        )
        if notification > now:
            return notification, prime
    return None, None


def start_scheduler() -> None:
    if scheduler.running:
        return
    scheduler.add_job(
        check_prime,
        "interval",
        minutes=1,
        id="prime-reminder",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )
    scheduler.start()
    logger.info("Scheduler started")

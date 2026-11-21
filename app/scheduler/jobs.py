import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app.bot import bot
from app.database.repository import SettingsRepository


KYIV_TZ = ZoneInfo("Europe/Kyiv")
logger = logging.getLogger("banderabot")


def get_due_prime(now: datetime):
    for day_offset in (0, 1):
        prime_date = now.date() + timedelta(days=day_offset)
        prime = SettingsRepository.get_today_prime(prime_date.weekday() + 1)
        if not prime:
            continue
        try:
            start_time = datetime.strptime(prime["start_time"], "%H:%M").time()
        except (TypeError, ValueError):
            logger.exception("Invalid prime start time in database")
            continue
        notification_time = (
            datetime.combine(prime_date, start_time, tzinfo=KYIV_TZ)
            - timedelta(minutes=30)
        )
        if now.strftime("%Y-%m-%d %H:%M") == notification_time.strftime(
            "%Y-%m-%d %H:%M"
        ):
            return prime_date, prime
    return None, None


async def check_prime() -> None:
    settings = SettingsRepository.get_settings()
    if not settings:
        logger.warning("Prime reminder skipped: settings not found")
        return
    if not settings["reminders_enabled"]:
        return
    if not settings["group_chat_id"]:
        logger.warning("Prime reminder skipped: group chat is not configured")
        return

    now = datetime.now(KYIV_TZ)
    prime_date, prime = get_due_prime(now)
    if prime_date is None or prime is None:
        return
    notification_date = prime_date.isoformat()
    if not SettingsRepository.mark_prime_notification_sent(
        notification_date,
        prime["start_time"],
    ):
        return

    try:
        await bot.send_message(
            chat_id=settings["group_chat_id"],
            text=(
                "🇺🇦 <b>ПРАЙМ 🇺🇦</b>\n\n"
                "🕗 Час:\n"
                f"{prime['start_time']} - {prime['end_time'] or '—'}\n\n"
                "⏰ До початку прайму залишилося 30 хвилин!\n\n"
                "Час заходити в гру!\n"
                "Всім бути онлайн! 🔥"
            ),
        )
    except Exception:
        SettingsRepository.remove_prime_notification(
            notification_date,
            prime["start_time"],
        )
        logger.exception("Failed to send prime reminder")
        raise

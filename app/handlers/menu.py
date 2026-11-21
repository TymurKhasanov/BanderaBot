import asyncio
import logging
from html import escape

from aiogram import F, Router
from aiogram.types import Message

from app.database.repository import SettingsRepository
from app.services.wiki import get_epics


router = Router()
logger = logging.getLogger("banderabot")


async def update_epics_timer(message: Message) -> None:
    elapsed = 0
    try:
        while True:
            await asyncio.sleep(3)
            elapsed += 3
            await message.edit_text(
                "⏳ Завантажую розклад епіків…\n"
                f"Минуло {elapsed} с · зазвичай 5–10 с"
            )
    except asyncio.CancelledError:
        pass
    except Exception:
        logger.debug("Could not update epics loading timer", exc_info=True)


@router.message(F.text == "📅 Прайм")
async def prime(message: Message) -> None:
    schedule = SettingsRepository.get_prime_schedule()
    await message.answer(
        escape(schedule) if schedule else "📅 Розклад прайму ще не встановлено."
    )


@router.message(F.text == "👹 Епіки")
async def epics(message: Message) -> None:
    loading = await message.answer(
        "⏳ Завантажую розклад епіків…\n"
        "Минуло 0 с · зазвичай 5–10 с"
    )
    task = asyncio.create_task(get_epics())
    timer = asyncio.create_task(update_epics_timer(loading))
    try:
        done, _ = await asyncio.wait({task}, timeout=35)
        if not done:
            task.cancel()
            raise TimeoutError("Epic refresh timed out")
        items = task.result()
    except Exception:
        logger.exception("Failed to retrieve epics")
        await loading.edit_text(
            "❌ Wiki не відповідає. Спробуйте повторити через хвилину."
        )
        return
    finally:
        timer.cancel()
        await timer
    if not items:
        await loading.edit_text("❌ Календар епіків наразі порожній.")
        return

    lines = ["<b>Найближчі епіки</b>", ""]
    for epic in items:
        lines.extend(
            (
                f'• <b><a href="{escape(str(epic["url"]), quote=True)}">'
                f'{escape(str(epic["name"]))}</a></b>',
                escape(str(epic["date"])),
                "",
            )
        )
    await loading.edit_text(
        "\n".join(lines).rstrip(),
        disable_web_page_preview=True,
    )


@router.message(F.text == "📢 Оголошення")
async def announcement(message: Message) -> None:
    text = SettingsRepository.get_announcement()
    await message.answer(
        escape(text) if text else "📢 Оголошень поки немає."
    )

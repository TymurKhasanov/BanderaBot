import logging
from html import escape

from aiogram import F, Router
from aiogram.types import Message

from app.database.repository import SettingsRepository
from app.services.wiki import get_epics


router = Router()
logger = logging.getLogger("banderabot")


@router.message(F.text == "📅 Прайм")
async def prime(message: Message) -> None:
    schedule = SettingsRepository.get_prime_schedule()
    await message.answer(
        escape(schedule) if schedule else "📅 Розклад прайму ще не встановлено."
    )


@router.message(F.text == "👹 Епіки")
async def epics(message: Message) -> None:
    try:
        items = await get_epics()
    except Exception:
        logger.exception("Failed to retrieve epics")
        await message.answer("❌ Не вдалося отримати розклад епіків.")
        return
    if not items:
        await message.answer("Не вдалося отримати розклад епіків.")
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
    await message.answer(
        "\n".join(lines).rstrip(),
        disable_web_page_preview=True,
    )


@router.message(F.text == "📢 Оголошення")
async def announcement(message: Message) -> None:
    text = SettingsRepository.get_announcement()
    await message.answer(
        escape(text) if text else "📢 Оголошень поки немає."
    )

import logging
from html import escape

from aiogram import F, Router
from aiogram.types import Message

from app.services.wiki import get_epics


router = Router()
logger = logging.getLogger("banderabot")


@router.message(F.text == "👹 Епіки")
async def show_epics(message: Message) -> None:
    try:
        epics = await get_epics()
    except Exception:
        logger.exception("Failed to retrieve epics")
        await message.answer("❌ Не вдалося отримати розклад епіків.")
        return

    if not epics:
        await message.answer("❌ Не вдалося отримати розклад епіків.")
        return

    lines = ["👹 <b>Найближчі епіки</b>", ""]
    for epic in epics:
        lines.extend(
            (
                f"🔸 <b>{escape(str(epic['name']))}</b>",
                f"🕒 {escape(str(epic['date']))}",
                f"🔗 {escape(str(epic['url']))}",
                "",
            )
        )
    await message.answer("\n".join(lines).rstrip(), disable_web_page_preview=True)

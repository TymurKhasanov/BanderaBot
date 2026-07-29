from aiogram import Router, F
from aiogram.types import Message

from app.services.wiki import get_epics

router = Router()


@router.message(F.text == "👹 Епіки")
async def show_epics(message: Message):
    try:
        epics = get_epics()

        if not epics:
            await message.answer("❌ Не вдалося отримати розклад епіків.")
            return

        text = "👹 <b>Найближчі епіки</b>\n\n"

        for epic in epics:
            text += (
                f"🔸 <b>{epic['name']}</b>\n"
                f"🕒 {epic['date']}\n"
                f"🔗 {epic['url']}\n\n"
            )

        await message.answer(
            text,
            disable_web_page_preview=True
        )

    except Exception as e:
        await message.answer(
            f"❌ Помилка отримання даних:\n<code>{e}</code>"
        )
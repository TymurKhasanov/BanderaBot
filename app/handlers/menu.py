from aiogram import F, Router
from aiogram.types import Message

from app.database.repository import SettingsRepository
from app.services.wiki import get_epics

router = Router()


@router.message(F.text == "📅 Прайм")
async def prime(message: Message):

    schedule = SettingsRepository.get_prime_schedule()

    if not schedule:
        await message.answer(
            "📅 Розклад прайму ще не встановлено."
        )
        return

    await message.answer(
        schedule
    )


@router.message(F.text == "👹 Епіки")
async def epics(message: Message):

    try:
        epics = get_epics()

        if not epics:
            await message.answer(
                "Не вдалося отримати розклад епіків."
            )
            return

        text = "<b>Найближчі епіки</b>\n\n"

        for epic in epics:
            text += (
                f'• <b><a href="{epic["url"]}">{epic["name"]}</a></b>\n'
                f'{epic["date"]}\n\n'
            )

        await message.answer(
            text,
            disable_web_page_preview=True
        )

    except Exception as e:
        await message.answer(
            f"Помилка: {e}"
        )


@router.message(F.text == "📢 Оголошення")
async def announcement(message: Message):

    text = SettingsRepository.get_announcement()

    if not text:
        await message.answer(
            "📢 Оголошень поки немає."
        )
        return

    await message.answer(
        text
    )
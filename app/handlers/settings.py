from aiogram import Router, F
from aiogram.types import Message

from app.database.repository import SettingsRepository
from app.keyboards.settings import settings_keyboard


router = Router()


@router.message(F.text == "⚙️ Налаштування")
async def settings(message: Message):

    # настройки только в личке
    if message.chat.type != "private":
        return


    settings = SettingsRepository.get_settings()


    text = f"""
⚙️ <b>Налаштування</b>

📅 Час прайму:
{settings["prime_time"] or "Не встановлено"}

🔔 Нагадування:
{"Увімкнено" if settings["reminders_enabled"] else "Вимкнено"}
"""


    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=settings_keyboard(True)
    )
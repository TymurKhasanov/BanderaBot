from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command

from app.keyboards.main import main_keyboard
from app.keyboards.admin import admin_main_keyboard
from app.config import OWNER_ID

router = Router()


@router.message(Command("start"))
async def start(message: Message):

    # На всякий случай убираем старую клавиатуру
    await message.answer(
        "Запуск...",
        reply_markup=ReplyKeyboardRemove()
    )

    # Личная переписка
    if message.chat.type == "private":

        if message.from_user.id == OWNER_ID:
            await message.answer(
                "🇺🇦 BanderaBot\n\n"
                "⚙️ Адмін меню",
                reply_markup=admin_main_keyboard
            )
        else:
            await message.answer(
                "🇺🇦 BanderaBot",
                reply_markup=main_keyboard
            )

    # Группа
    else:
        await message.answer(
            "🇺🇦 BanderaBot\n\n"
            "Оберіть потрібний розділ.",
            reply_markup=main_keyboard
        )
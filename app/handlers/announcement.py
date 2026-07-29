from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatType

from app.database.repository import SettingsRepository
from app.states.announcement import AnnouncementStates


router = Router()


@router.message(Command("setannounce"))
async def set_announce_start(
    message: Message,
    state: FSMContext
):
    # Только группа
    if message.chat.type == ChatType.PRIVATE:
        await message.answer(
            "❌ Цю команду можна використовувати лише в групі."
        )
        return

    # Проверяем права пользователя
    member = await message.bot.get_chat_member(
        message.chat.id,
        message.from_user.id
    )

    if member.status not in (
        "creator",
        "administrator"
    ):
        await message.answer(
            "❌ Лише адміністратор групи може змінювати оголошення."
        )
        return

    await state.set_state(
        AnnouncementStates.waiting_text
    )

    await message.answer(
        "✏️ Введіть текст оголошення:"
    )


@router.message(AnnouncementStates.waiting_text)
async def save_announcement(
    message: Message,
    state: FSMContext
):
    SettingsRepository.update_announcement(
        message.text
    )

    await state.clear()

    await message.answer(
        "✅ Оголошення успішно оновлено!"
    )
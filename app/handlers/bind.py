from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ChatType

from app.database.repository import SettingsRepository


router = Router()


@router.message(Command("bind"))
async def bind_group(message: Message):

    if message.chat.type == ChatType.PRIVATE:
        await message.answer(
            "❌ Цю команду можна використовувати лише в групі."
        )
        return

    member = await message.bot.get_chat_member(
        message.chat.id,
        message.from_user.id
    )

    if member.status not in ("creator", "administrator"):
        await message.answer(
            "❌ Лише адміністратор групи може прив'язати чат."
        )
        return

    SettingsRepository.update_group_chat(
        message.chat.id
    )

    await message.answer(
        "✅ Групу успішно прив'язано!\n\n"
        "Усі нагадування про прайм будуть надсилатися сюди."
    )
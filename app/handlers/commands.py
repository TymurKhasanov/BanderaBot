from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router()


@router.message(Command("commands"))
async def commands_list(message: Message):

    if message.chat.type == "private":
        await message.answer(
            "❌ Ця команда доступна тільки в групі."
        )
        return


    member = await message.bot.get_chat_member(
        message.chat.id,
        message.from_user.id
    )


    if member.status not in (
        "creator",
        "administrator"
    ):
        await message.answer(
            "❌ Лише адміністратори можуть переглядати команди."
        )
        return


    text = """
⚙️ <b>Адмін команди</b>

🔗 /bind
Прив'язати групу для нагадувань

📅 /setprime
Змінити розклад прайму

👹 /setepics
Змінити розклад епіків

📢 /setannounce
Змінити оголошення

⚙️ /commands
Показати список команд
"""


    await message.answer(
        text,
        parse_mode="HTML"
    )
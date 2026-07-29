from aiogram import Router
from aiogram.types import CallbackQuery

from app.config import OWNER_ID


router = Router()


@router.callback_query(
    lambda callback: callback.data == "show_commands"
)
async def show_commands(
    callback: CallbackQuery
):

    if callback.from_user.id != OWNER_ID:

        await callback.answer(
            "❌ Тільки для адміністраторів",
            show_alert=True
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

📋 /commands
Показати список команд
"""


    await callback.message.answer(
        text,
        parse_mode="HTML"
    )


    await callback.answer()
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.database.repository import SettingsRepository
from app.states.prime import PrimeStates


router = Router()


@router.message(Command("setprime"))
async def set_prime(
    message: Message,
    state: FSMContext
):

    if message.chat.type == "private":
        await message.answer(
            "❌ Цю команду можна використовувати тільки в групі."
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
            "❌ Лише адміністратор може змінювати розклад."
        )
        return


    await state.set_state(
        PrimeStates.waiting_schedule
    )

    await message.answer(
        "✏️ Введіть розклад прайму на тиждень:"
    )


@router.message(PrimeStates.waiting_schedule)
async def save_prime(
    message: Message,
    state: FSMContext
):

    SettingsRepository.update_prime_schedule(
        message.text
    )

    await state.clear()

    await message.answer(
        "✅ Розклад прайму оновлено!"
    )
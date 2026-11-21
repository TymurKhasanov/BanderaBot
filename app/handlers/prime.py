from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.services.prime import save_prime_schedule
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

    if not message.text or not message.text.strip():
        await message.answer("❌ Надішліть розклад текстом.")
        return

    try:
        save_prime_schedule(message.text)
    except ValueError as exc:
        await message.answer(f"❌ {exc}")
        return

    await state.clear()

    await message.answer(
        "✅ Розклад прайму оновлено!"
    )
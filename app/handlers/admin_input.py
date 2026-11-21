import logging
from html import escape

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.database.repository import SettingsRepository
from app.services.prime import save_prime_schedule
from app.states.admin import AdminStates


router = Router()
logger = logging.getLogger("banderabot")


def require_text(message: Message) -> str | None:
    return message.text.strip() if message.text and message.text.strip() else None


@router.message(AdminStates.waiting_prime_time)
async def save_prime_time(message: Message, state: FSMContext) -> None:
    text = require_text(message)
    if text is None:
        await message.answer("❌ Надішліть текст розкладу.")
        return

    try:
        save_prime_schedule(text)
    except ValueError as exc:
        await message.answer(f"❌ {escape(str(exc))}")
        return

    settings = SettingsRepository.get_settings()
    group_id = settings["group_chat_id"] if settings else None
    if group_id:
        try:
            await message.bot.send_message(
                group_id,
                "📅 <b>Оновлено розклад прайму</b>\n\n"
                f"{escape(text)}",
            )
        except Exception:
            logger.exception("Failed to notify bound group about prime update")

    await state.clear()
    await message.answer("✅ Розклад прайму оновлено!")


@router.message(AdminStates.waiting_epics)
async def save_epics(message: Message, state: FSMContext) -> None:
    text = require_text(message)
    if text is None:
        await message.answer("❌ Надішліть розклад епіків.")
        return

    SettingsRepository.update_epics_schedule(text)
    await state.clear()
    await message.answer("✅ Розклад епіків оновлено!")


@router.message(AdminStates.waiting_announcement)
async def save_announcement(message: Message, state: FSMContext) -> None:
    text = require_text(message)
    if text is None:
        await message.answer("❌ Надішліть текст оголошення.")
        return

    SettingsRepository.update_announcement(text)
    await state.clear()
    await message.answer("✅ Оголошення оновлено!")

import logging
from html import escape

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.services.experience import (
    calculate_remaining_exp,
    format_exp,
    parse_level,
    parse_percent,
)
from app.states.experience import ExperienceStates


router = Router()
logger = logging.getLogger("banderabot")


@router.message(F.text == "📈 EXP")
async def exp_menu(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(ExperienceStates.waiting_level)
    await message.answer(
        "📈 <b>Розрахунок EXP</b>\n\n"
        "Введіть ваш поточний рівень від 1 до 74.\n"
        "Наприклад: <code>68</code>"
    )


@router.message(ExperienceStates.waiting_level)
async def save_exp_level(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("❌ Надішліть рівень текстом.")
        return
    try:
        level = parse_level(message.text)
    except ValueError as exc:
        await message.answer(f"❌ {escape(str(exc))}")
        return

    await state.update_data(exp_level=level)
    await state.set_state(ExperienceStates.waiting_percent)
    await message.answer(
        f"Рівень <b>{level}</b> збережено.\n"
        "Введіть поточний процент досвіду до наступного рівня.\n"
        "Наприклад: <code>53,5</code>"
    )


@router.message(ExperienceStates.waiting_percent)
async def calculate_exp(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("❌ Надішліть процент досвіду текстом.")
        return
    try:
        percent = parse_percent(message.text)
    except ValueError as exc:
        await message.answer(f"❌ {escape(str(exc))}")
        return

    data = await state.get_data()
    level = data.get("exp_level")
    if not isinstance(level, int):
        await state.clear()
        await state.set_state(ExperienceStates.waiting_level)
        await message.answer("Сесія розрахунку скинулася. Введіть рівень ще раз.")
        return

    try:
        result = calculate_remaining_exp(level, percent)
    except (KeyError, ValueError, OSError):
        logger.exception("Failed to calculate EXP remainder")
        await message.answer("❌ Не вдалося прочитати таблицю досвіду.")
        await state.clear()
        return

    percent_text = format(percent, "f").rstrip("0").rstrip(".") or "0"
    await message.answer(
        "📈 <b>Результат</b>\n\n"
        f"Поточний рівень: <b>{level}</b>\n"
        f"Прогрес: <b>{escape(percent_text)}%</b>\n"
        f"Наступний рівень: <b>{result['next_level']}</b>\n\n"
        f"За рівень потрібно: <b>{format_exp(result['required'])} EXP</b>\n"
        f"Вже набрано приблизно: <b>{format_exp(result['earned'])} EXP</b>\n"
        f"Залишилося: <b>{format_exp(result['remaining'])} EXP</b>"
    )
    await state.clear()

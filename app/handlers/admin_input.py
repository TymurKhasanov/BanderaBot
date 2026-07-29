from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import re

from app.states.admin import AdminStates
from app.database.repository import SettingsRepository


router = Router()


DAYS = {
    "Понеділок": 1,
    "Вівторок": 2,
    "Середа": 3,
    "Четвер": 4,
    "П’ятниця": 5,
    "П'ятниця": 5,
    "Субота": 6,
    "Неділя": 7,
}



@router.message(AdminStates.waiting_prime_time)
async def save_prime_time(
    message: Message,
    state: FSMContext
):

    text = message.text.strip()


    # Сохраняем красивый текст для показа в группе
    SettingsRepository.update_prime_time(
        text
    )


    # Чистим старое расписание
    SettingsRepository.clear_prime_schedule()


    # Разбираем дни недели
    for line in text.split("\n"):

        line = line.strip()

        if not line:
            continue


        day_number = None


        for day_name, number in DAYS.items():

            if line.startswith(day_name):

                day_number = number
                break


        if not day_number:
            continue


        times = re.findall(
            r"\d{2}:\d{2}",
            line
        )


        if len(times) >= 2:

            SettingsRepository.add_prime_day(
                day_number,
                times[0],
                times[1]
            )


    # Уведомление в группу
    settings = SettingsRepository.get_settings()

    group_id = settings["group_chat_id"]


    if group_id:

        await message.bot.send_message(
            group_id,
            f"""
📅 <b>Оновлено розклад прайму</b>

{text}
""",
            parse_mode="HTML"
        )


    await state.clear()


    await message.answer(
        "✅ Час прайму оновлено!"
    )



@router.message(AdminStates.waiting_epics)
async def save_epics(
    message: Message,
    state: FSMContext
):

    SettingsRepository.update_epics_schedule(
        message.text
    )

    await state.clear()

    await message.answer(
        "✅ Розклад епіків оновлено!"
    )



@router.message(AdminStates.waiting_announcement)
async def save_announcement(
    message: Message,
    state: FSMContext
):

    SettingsRepository.update_announcement(
        message.text
    )

    await state.clear()

    await message.answer(
        "✅ Оголошення оновлено!"
    )
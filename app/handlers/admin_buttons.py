from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.database.repository import SettingsRepository
from app.states.admin import AdminStates
from app.config import OWNER_ID


router = Router()

print("ADMIN BUTTONS LOADED")


async def check_admin(callback: CallbackQuery) -> bool:

    # Владелец бота
    if callback.from_user.id == OWNER_ID:
        return True

    # Админы группы
    if callback.message and callback.message.chat.type != "private":

        member = await callback.bot.get_chat_member(
            callback.message.chat.id,
            callback.from_user.id
        )

        if member.status in (
            "creator",
            "administrator"
        ):
            return True

    await callback.answer(
        "❌ Тільки для адміністраторів",
        show_alert=True
    )

    return False



# =========================
# ПРАЙМ
# =========================

@router.callback_query(
    lambda c: c.data in (
        "change_prime_time",
        "admin_prime_time"
    )
)
async def change_prime_time(
    callback: CallbackQuery,
    state: FSMContext
):

    print("CLICK:", callback.data)

    if not await check_admin(callback):
        return


    await state.set_state(
        AdminStates.waiting_prime_time
    )


    await callback.message.answer(
        "📅 Введіть новий час прайму:"
    )


    await callback.answer()



# =========================
# ЭПИКИ
# =========================

@router.callback_query(
    lambda c: c.data in (
        "change_epics",
        "admin_epics"
    )
)
async def change_epics(
    callback: CallbackQuery,
    state: FSMContext
):

    print("CLICK:", callback.data)

    if not await check_admin(callback):
        return


    await state.set_state(
        AdminStates.waiting_epics
    )


    await callback.message.answer(
        "👹 Введіть новий розклад епіків:"
    )


    await callback.answer()



# =========================
# НАПОМИНАНИЯ
# =========================

@router.callback_query(
    lambda c: c.data in (
        "toggle_reminders",
        "admin_reminders"
    )
)
async def toggle_reminders(
    callback: CallbackQuery
):

    print("CLICK:", callback.data)

    if not await check_admin(callback):
        return


    settings = SettingsRepository.get_settings()

    current = bool(
        settings["reminders_enabled"]
    )


    SettingsRepository.set_reminders(
        not current
    )


    await callback.message.answer(
        f"""
🔔 Нагадування:

{"Увімкнено" if not current else "Вимкнено"}
"""
    )


    await callback.answer()



# =========================
# ОБЪЯВЛЕНИЕ
# =========================

@router.callback_query(
    lambda c: c.data in (
        "change_announcement",
        "admin_announcement"
    )
)
async def change_announcement(
    callback: CallbackQuery,
    state: FSMContext
):

    print("CLICK:", callback.data)

    if not await check_admin(callback):
        return


    await state.set_state(
        AdminStates.waiting_announcement
    )


    await callback.message.answer(
        "📢 Введіть нове оголошення:"
    )


    await callback.answer()



# =========================
# ПРИВЯЗКА ГРУППЫ
# =========================

@router.callback_query(
    lambda c: c.data in (
        "bind_group",
        "admin_bind"
    )
)
async def bind_group(
    callback: CallbackQuery
):

    print("CLICK:", callback.data)

    if not await check_admin(callback):
        return


    if callback.message.chat.type == "private":

        await callback.answer(
            "❌ Виконайте прив'язку з групи",
            show_alert=True
        )

        return


    SettingsRepository.update_group_chat(
        callback.message.chat.id
    )


    await callback.message.answer(
        "✅ Групу успішно прив'язано!"
    )


    await callback.answer()
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def settings_keyboard(
    is_admin: bool
) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    if is_admin:

        builder.button(
            text="📅 Змінити час прайму",
            callback_data="change_prime_time"
        )

        builder.button(
            text="👹 Змінити розклад епіків",
            callback_data="change_epics"
        )

        builder.button(
            text="🔔 Вкл/Викл нагадування",
            callback_data="toggle_reminders"
        )

        builder.button(
            text="📢 Змінити оголошення",
            callback_data="change_announcement"
        )

        builder.button(
            text="🔗 Прив'язати групу",
            callback_data="bind_group"
        )

        builder.button(
            text="📋 Команди",
            callback_data="show_commands"
        )

    builder.adjust(1)

    return builder.as_markup()
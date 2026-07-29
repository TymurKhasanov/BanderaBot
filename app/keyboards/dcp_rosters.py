from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def rosters_keyboard(
    rosters: list,
    prefix: str = "roster",
) -> InlineKeyboardMarkup:
    keyboard = []

    for roster in rosters:
        keyboard.append([
            InlineKeyboardButton(
                text=roster["name"],
                callback_data=f"{prefix}:{roster['id']}"
            )
        ])

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )
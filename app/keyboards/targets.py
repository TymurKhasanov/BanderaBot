from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def targets_rosters_keyboard(rosters: dict) -> InlineKeyboardMarkup:
    keyboard = []

    sorted_rosters = sorted(
        rosters.items(),
        key=lambda item: item[1]["name"].lower(),
    )

    for roster_id, roster in sorted_rosters:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"📋 {roster['name']}",
                    callback_data=f"targets:roster:{roster_id}",
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="dcp",
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )


def targets_keyboard(
    targets: list,
    roster_id: str,
) -> InlineKeyboardMarkup:

    keyboard = []

    for target in targets:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"📋 /target {target['nickname']}",
                    callback_data=f"target:{target['id']}",
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="⬅️ До команд",
                callback_data="targets",
            )
        ]
    )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="🏠 ДЦП",
                callback_data="dcp",
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )
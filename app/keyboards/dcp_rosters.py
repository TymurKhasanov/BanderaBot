from typing import Any

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


SORT_LABELS = {
    "name": "🔤 Назва",
    "level": "📈 Рівень",
    "normal": "💵 DKP",
    "epic": "💎 Epic DKP",
}
FILTER_LABELS = {
    "all": "Усі",
    "phys": "⚔️ Фіз",
    "mag": "🪄 Маг",
}


def callback_data(prefix: str, roster_id: object) -> str:
    value = f"{prefix}:{roster_id}"
    if len(value.encode("utf-8")) > 64:
        raise ValueError("Telegram callback_data exceeds 64 bytes")
    return value


def roster_list_keyboard(
    rosters: list[dict[str, Any]],
    *,
    sort: str = "name",
    roster_filter: str = "all",
) -> InlineKeyboardMarkup:
    keyboard: list[list[InlineKeyboardButton]] = []
    for index, roster in enumerate(rosters, start=1):
        roster_id = roster.get("id")
        if roster_id is None:
            raise ValueError("DCP roster is missing id")
        name = str(roster.get("name") or "Без назви")
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{index}. {name}",
                    callback_data=callback_data("roster", roster_id),
                )
            ]
        )

    filter_buttons = []
    for key, label in FILTER_LABELS.items():
        selected = "✓ " if key == roster_filter else ""
        filter_buttons.append(
            InlineKeyboardButton(
                text=f"{selected}{label}",
                callback_data=f"rosters:{sort}:{key}",
            )
        )
    keyboard.append(filter_buttons)

    sort_buttons = []
    for key, label in SORT_LABELS.items():
        selected = "✓ " if key == sort else ""
        sort_buttons.append(
            InlineKeyboardButton(
                text=f"{selected}{label}",
                callback_data=f"rosters:{key}:{roster_filter}",
            )
        )
    keyboard.extend([sort_buttons[:2], sort_buttons[2:]])
    keyboard.append(
        [
            InlineKeyboardButton(
                text="🔄 Оновити",
                callback_data=f"rosters:{sort}:{roster_filter}:refresh",
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def roster_card_keyboard(roster_id: object) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💰 Баланс",
                    callback_data=callback_data("balance", roster_id),
                ),
                InlineKeyboardButton(
                    text="🎯 Цілі",
                    callback_data=callback_data("targets:roster", roster_id),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Оновити",
                    callback_data=callback_data("roster", roster_id),
                ),
                InlineKeyboardButton(
                    text="⬅️ Усі ростери",
                    callback_data="rosters:name:all",
                ),
            ],
        ]
    )


def balance_list_keyboard(
    rosters: list[dict[str, Any]],
) -> InlineKeyboardMarkup:
    keyboard = []
    for roster in rosters:
        roster_id = roster.get("id")
        if roster_id is None:
            raise ValueError("DCP roster is missing id")
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=str(roster.get("name") or "Без назви"),
                    callback_data=callback_data("balance", roster_id),
                )
            ]
        )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def rosters_keyboard(
    rosters: list[dict[str, Any]],
    prefix: str = "roster",
) -> InlineKeyboardMarkup:
    if prefix == "balance":
        return balance_list_keyboard(rosters)
    return roster_list_keyboard(rosters)

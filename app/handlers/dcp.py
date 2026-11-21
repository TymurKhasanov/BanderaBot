import logging
from html import escape
from typing import Any

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from app.keyboards.dcp import dcp_keyboard
from app.keyboards.dcp_rosters import (
    roster_card_keyboard,
    roster_list_keyboard,
    rosters_keyboard,
)
from app.keyboards.main import main_keyboard
from app.services.dcp_api import dcp_api


router = Router()
logger = logging.getLogger("banderabot")

CLASS_ICONS = {
    "HAWKEYE": "🏹",
    "SILVER_RANGER": "🏹",
    "PHANTOM_RANGER": "🏹",
    "TREASURE_HUNTER": "🗡️",
    "PLAINS_WALKER": "🗡️",
    "ABYSS_WALKER": "🗡️",
    "PALADIN": "🛡️",
    "DARK_AVENGER": "🛡️",
    "TEMPLE_KNIGHT": "🛡️",
    "SHILLIEN_KNIGHT": "🛡️",
    "GLADIATOR": "⚔️",
    "WARLORD": "⚔️",
    "DESTROYER": "⚔️",
    "TYRANT": "⚔️",
    "SORCERER": "🪄",
    "SPELLSINGER": "🪄",
    "SPELLHOWLER": "🪄",
    "NECROMANCER": "🪄",
    "BISHOP": "❤️",
    "CARDINAL": "❤️",
    "PROPHET": "✨",
    "ELDER": "✨",
    "SHILLIEN_ELDER": "✨",
    "SWORDSINGER": "🎵",
    "BLADEDANCER": "💃",
    "WARCRYER": "📯",
    "OVERLORD": "📯",
    "TERRAMANCER": "🌋",
    "BOUNTY_HUNTER": "🗡️",
    "WARLOCK": "🐺",
    "ELEMENTAL_SUMMONER": "🐺",
    "PHANTOM_SUMMONER": "🐺",
}

ROLE_GROUPS = {
    "🏹 DD": {
        "HAWKEYE",
        "SILVER_RANGER",
        "PHANTOM_RANGER",
        "TREASURE_HUNTER",
        "PLAINS_WALKER",
        "ABYSS_WALKER",
        "GLADIATOR",
        "WARLORD",
        "DESTROYER",
        "TYRANT",
        "SORCERER",
        "SPELLSINGER",
        "SPELLHOWLER",
        "NECROMANCER",
        "TERRAMANCER",
        "BOUNTY_HUNTER",
    },
    "🛡️ Танк": {
        "PALADIN",
        "DARK_AVENGER",
        "TEMPLE_KNIGHT",
        "SHILLIEN_KNIGHT",
    },
    "✨ Сапорт": {
        "PROPHET",
        "ELDER",
        "SHILLIEN_ELDER",
        "SWORDSINGER",
        "BLADEDANCER",
        "WARCRYER",
        "OVERLORD",
        "WARLOCK",
        "ELEMENTAL_SUMMONER",
        "PHANTOM_SUMMONER",
    },
    "❤️ Хіл": {"BISHOP", "CARDINAL"},
}


def balance_value(value: object) -> str:
    if value is None:
        return "0"
    if isinstance(value, float) and value.is_integer():
        return f"{int(value):,}".replace(",", " ")
    if isinstance(value, int):
        return f"{value:,}".replace(",", " ")
    return escape(str(value))


def average_level(members: list[dict[str, Any]]) -> str:
    levels = [
        float(member["level"])
        for member in members
        if isinstance(member.get("level"), (int, float))
    ]
    return f"{sum(levels) / len(levels):.1f}" if levels else "—"


def member_grade(member: dict[str, Any]) -> str:
    grade = str(member.get("grade") or "—")
    return grade


def roster_summary(
    roster: dict[str, Any],
    *,
    index: int | None = None,
) -> str:
    name = escape(str(roster.get("name") or "Без назви"))
    members = roster.get("members") or []
    pack_kind = str(roster.get("packKind") or "").upper()
    pack_icon = "🪄 Маг" if pack_kind == "MAG" else "⚔️ Фіз"
    balances = roster.get("balances") or {}
    normal = (balances.get("normal") or {}).get("available")
    epic = (balances.get("epic") or {}).get("available")
    prefix = f"{index}. " if index is not None else ""
    return (
        f"{prefix}<b>{name}</b>\n"
        f"{pack_icon} · 👥 {len(members)}/9 · 📈 Lv {average_level(members)}\n"
        f"💵 {balance_value(normal)} · 💎 {balance_value(epic)}"
    )


def filtered_rosters(
    rosters: list[dict[str, Any]],
    sort: str,
    roster_filter: str,
) -> list[dict[str, Any]]:
    if roster_filter in {"phys", "mag"}:
        wanted = roster_filter.upper()
        rosters = [
            roster
            for roster in rosters
            if str(roster.get("packKind", "")).upper() == wanted
        ]

    def normal_balance(roster: dict[str, Any]) -> float:
        value = ((roster.get("balances") or {}).get("normal") or {}).get(
            "available",
            0,
        )
        return float(value or 0)

    def epic_balance(roster: dict[str, Any]) -> float:
        value = ((roster.get("balances") or {}).get("epic") or {}).get(
            "available",
            0,
        )
        return float(value or 0)

    if sort == "level":
        return sorted(
            rosters,
            key=lambda roster: float(average_level(roster.get("members") or [])
                                    .replace("—", "0")),
            reverse=True,
        )
    if sort == "normal":
        return sorted(rosters, key=normal_balance, reverse=True)
    if sort == "epic":
        return sorted(rosters, key=epic_balance, reverse=True)
    return sorted(
        rosters,
        key=lambda roster: str(roster.get("name") or "").casefold(),
    )


def roster_list_text(
    rosters: list[dict[str, Any]],
    sort: str,
    roster_filter: str,
) -> str:
    visible = filtered_rosters(rosters, sort, roster_filter)
    summaries = [
        roster_summary(roster, index=index)
        for index, roster in enumerate(visible, start=1)
    ]
    filter_title = {"all": "усі", "phys": "фізичні", "mag": "магічні"}[
        roster_filter
    ]
    return (
        f"👥 <b>Ростери клану</b> · {len(visible)}/{len(rosters)} ({filter_title})\n\n"
        + "\n\n".join(summaries)
    )


def roster_detail_text(roster: dict[str, Any]) -> str:
    members = roster.get("members") or []
    grades = [member_grade(member) for member in members]
    grades_text = " / ".join(sorted(set(grades))) or "—"
    pack_kind = str(roster.get("packKind") or "").upper()
    pack_icon = "🪄 Магічна пачка" if pack_kind == "MAG" else "⚔️ Фізична пачка"
    coefficient = balance_value(roster.get("coefficient") or 1)
    approval = (
        "✅ Грейди підтверджені"
        if roster.get("gradeApproved")
        else "⏳ Грейди очікують перевірки"
    )
    screenshot = (
        "📷 Скріншот обовʼязковий"
        if roster.get("screenshotRequired")
        else "📷 Скріншот необовʼязковий"
    )
    balances = roster.get("balances") or {}
    normal = balances.get("normal") or {}
    epic = balances.get("epic") or {}

    lines = [
        f"👥 <b>{escape(str(roster.get('name') or 'Без назви'))}</b>",
        (
            f"{pack_icon} · 👥 {len(members)}/9 · "
            f"📈 середній Lv {average_level(members)}"
        ),
        f"🏅 Грейди: {escape(grades_text)} · коефіцієнт ×{coefficient}",
        approval,
        screenshot,
        "",
        (
            f"💵 DKP: {balance_value(normal.get('available'))} доступно"
            f" · {balance_value(normal.get('reserved'))} в резерві"
        ),
        (
            f"💎 Epic DKP: {balance_value(epic.get('available'))} доступно"
            f" · {balance_value(epic.get('reserved'))} в резерві"
        ),
    ]

    grouped: dict[str, list[dict[str, Any]]] = {
        role: [] for role in ROLE_GROUPS
    }
    grouped["🎒 Інше"] = []
    for member in members:
        class_name = str(member.get("className") or "")
        role = next(
            (
                role_name
                for role_name, classes in ROLE_GROUPS.items()
                if class_name in classes
            ),
            "🎒 Інше",
        )
        grouped[role].append(member)

    for role, role_members in grouped.items():
        if not role_members:
            continue
        lines.extend(("", f"<b>{role}</b>"))
        for member in role_members:
            class_name = str(member.get("className") or "Unknown")
            class_title = class_name.replace("_", " ").title()
            lines.append(
                f"{CLASS_ICONS.get(class_name, '•')} "
                f"<b>{escape(str(member.get('nickname') or 'Unknown'))}</b>"
                f" — {escape(class_title)} · Lv {escape(str(member.get('level', '?')))}"
                f" · {escape(member_grade(member))}"
            )
    return "\n".join(lines)


async def answer_error(
    event: Message | CallbackQuery,
    operation: str,
) -> None:
    logger.exception("DCP operation failed: %s", operation)
    message = "❌ Сервіс ДЦП тимчасово недоступний."
    if isinstance(event, CallbackQuery):
        await event.answer(message, show_alert=True)
    else:
        await event.answer(message)


@router.message(F.text == "📊 ДЦП")
async def dcp_menu(message: Message) -> None:
    await message.answer(
        "📊 <b>Меню ДЦП</b>\n\nОберіть потрібний розділ:",
        reply_markup=dcp_keyboard,
    )


@router.callback_query(F.data == "dcp")
async def dcp_menu_callback(callback: CallbackQuery) -> None:
    if callback.message is None:
        await callback.answer("Повідомлення недоступне.", show_alert=True)
        return
    await callback.message.answer(
        "📊 <b>Меню ДЦП</b>\n\nОберіть потрібний розділ:",
        reply_markup=dcp_keyboard,
    )
    await callback.answer()


@router.message(F.text == "👥 Ростери")
async def rosters(message: Message) -> None:
    try:
        data = await dcp_api.get_rosters()
    except Exception:
        await answer_error(message, "get rosters")
        return
    if not data:
        await message.answer("Ростерів не знайдено.")
        return
    visible = filtered_rosters(data, "name", "all")
    await message.answer(
        roster_list_text(data, "name", "all"),
        reply_markup=roster_list_keyboard(visible),
    )


@router.callback_query(F.data.startswith("rosters:"))
async def rosters_list_callback(callback: CallbackQuery) -> None:
    if callback.message is None or not callback.data:
        await callback.answer("Повідомлення недоступне.", show_alert=True)
        return
    parts = callback.data.split(":")
    sort = parts[1] if len(parts) > 1 and parts[1] in {"name", "level", "normal", "epic"} else "name"
    roster_filter = parts[2] if len(parts) > 2 and parts[2] in {"all", "phys", "mag"} else "all"
    try:
        data = await dcp_api.get_rosters()
    except Exception:
        await answer_error(callback, "refresh rosters")
        return
    visible = filtered_rosters(data, sort, roster_filter)
    await callback.message.edit_text(
        roster_list_text(data, sort, roster_filter),
        reply_markup=roster_list_keyboard(
            visible,
            sort=sort,
            roster_filter=roster_filter,
        ),
    )
    await callback.answer("Оновлено" if len(parts) > 3 else "")


@router.callback_query(F.data.startswith("roster:"))
async def roster_info(callback: CallbackQuery) -> None:
    if callback.message is None or not callback.data:
        await callback.answer("Повідомлення недоступне.", show_alert=True)
        return
    roster_id = callback.data.partition(":")[2]
    try:
        data = await dcp_api.get_rosters()
    except Exception:
        await answer_error(callback, "get roster")
        return
    roster = next((item for item in data if str(item.get("id")) == roster_id), None)
    if roster is None:
        await callback.answer("Ростер не знайдено.", show_alert=True)
        return
    await callback.message.edit_text(
        roster_detail_text(roster),
        reply_markup=roster_card_keyboard(roster_id),
    )
    await callback.answer()


@router.message(F.text == "💰 Баланс")
async def balance(message: Message) -> None:
    try:
        data = await dcp_api.get_rosters()
    except Exception:
        await answer_error(message, "get balances")
        return
    if not data:
        await message.answer("Ростерів не знайдено.")
        return
    await message.answer(
        "💰 <b>Оберіть ростер</b>",
        reply_markup=rosters_keyboard(data, prefix="balance"),
    )


@router.callback_query(F.data.startswith("balance:"))
async def roster_balance(callback: CallbackQuery) -> None:
    if callback.message is None or not callback.data:
        await callback.answer("Повідомлення недоступне.", show_alert=True)
        return
    roster_id = callback.data.partition(":")[2]
    try:
        data = await dcp_api.get_rosters()
    except Exception:
        await answer_error(callback, "get balance")
        return
    roster = next((item for item in data if str(item.get("id")) == roster_id), None)
    if roster is None:
        await callback.answer("Ростер не знайдено.", show_alert=True)
        return

    balances = roster.get("balances") or {}
    normal = balances.get("normal") or {}
    epic = balances.get("epic") or {}
    text = (
        f"🏰 <b>{escape(str(roster.get('name') or 'Без назви'))}</b>\n\n"
        "💵 <b>Звичайний баланс</b>\n"
        f"🟢 Доступно: {balance_value(normal.get('available'))}\n"
        f"🟡 Зарезервовано: {balance_value(normal.get('reserved'))}\n"
        f"⚪ Всього: {balance_value(normal.get('total'))}\n\n"
        "💎 <b>Епічний баланс</b>\n"
        f"🟢 Доступно: {balance_value(epic.get('available'))}\n"
        f"🟡 Зарезервовано: {balance_value(epic.get('reserved'))}\n"
        f"⚪ Всього: {balance_value(epic.get('total'))}"
    )
    await callback.message.edit_text(
        text,
        reply_markup=roster_card_keyboard(roster_id),
    )
    await callback.answer()


@router.message(F.text == "⬅️ Назад")
async def back_to_main(message: Message) -> None:
    await message.answer("Головне меню", reply_markup=main_keyboard)

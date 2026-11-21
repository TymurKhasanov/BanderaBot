import logging
from html import escape

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from app.keyboards.targets import targets_keyboard, targets_rosters_keyboard
from app.services.targets import (
    get_roster_targets,
    get_rosters_with_targets,
    get_targets,
)


router = Router()
logger = logging.getLogger("banderabot")

CLASS_NAMES = {
    "HAWKEYE": "Hawkeye",
    "SILVER_RANGER": "Silver Ranger",
    "PHANTOM_RANGER": "Phantom Ranger",
    "TREASURE_HUNTER": "Treasure Hunter",
    "PLAINS_WALKER": "Plains Walker",
    "ABYSS_WALKER": "Abyss Walker",
    "PALADIN": "Paladin",
    "DARK_AVENGER": "Dark Avenger",
    "TEMPLE_KNIGHT": "Temple Knight",
    "SHILLIEN_KNIGHT": "Shillien Knight",
    "GLADIATOR": "Gladiator",
    "WARLORD": "Warlord",
    "DESTROYER": "Destroyer",
    "TYRANT": "Tyrant",
    "SORCERER": "Sorcerer",
    "SPELLSINGER": "Spellsinger",
    "SPELLHOWLER": "Spellhowler",
    "NECROMANCER": "Necromancer",
    "BISHOP": "Bishop",
    "CARDINAL": "Cardinal",
    "PROPHET": "Prophet",
    "ELDER": "Elven Elder",
    "SHILLIEN_ELDER": "Shillien Elder",
    "SWORDSINGER": "Swordsinger",
    "BLADEDANCER": "Bladedancer",
    "WARLOCK": "Warlock",
    "ELEMENTAL_SUMMONER": "Elemental Summoner",
    "PHANTOM_SUMMONER": "Phantom Summoner",
}


async def report_error(event: Message | CallbackQuery) -> None:
    logger.exception("Failed to retrieve DCP targets")
    if isinstance(event, CallbackQuery):
        await event.answer("❌ Не вдалося отримати цілі.", show_alert=True)
    else:
        await event.answer("❌ Не вдалося отримати цілі.")


@router.message(F.text == "🎯 Цілі")
async def targets_menu(message: Message) -> None:
    try:
        rosters = await get_rosters_with_targets()
    except Exception:
        await report_error(message)
        return
    if not rosters:
        await message.answer("🎯 Цілі не знайдено.")
        return
    await message.answer(
        "🎯 <b>Оберіть команду</b>",
        reply_markup=targets_rosters_keyboard(rosters),
    )


@router.callback_query(F.data == "targets")
async def targets_back(callback: CallbackQuery) -> None:
    if callback.message is None:
        await callback.answer("Повідомлення недоступне.", show_alert=True)
        return
    try:
        rosters = await get_rosters_with_targets()
    except Exception:
        await report_error(callback)
        return
    if not rosters:
        await callback.answer("Цілі не знайдено.", show_alert=True)
        return
    await callback.message.edit_text(
        "🎯 <b>Оберіть команду</b>",
        reply_markup=targets_rosters_keyboard(rosters),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("targets:roster:"))
async def roster_selected(callback: CallbackQuery) -> None:
    if callback.message is None or not callback.data:
        await callback.answer("Повідомлення недоступне.", show_alert=True)
        return
    roster_id = callback.data.split(":", 2)[2]
    try:
        roster = await get_roster_targets(roster_id)
    except Exception:
        await report_error(callback)
        return
    if not roster:
        await callback.answer("Команду не знайдено.", show_alert=True)
        return

    targets = roster["targets"]
    title = escape(str(roster["name"]))
    if not targets:
        await callback.message.edit_text(f"🎯 <b>{title}</b>\n\nЦілей немає.")
        await callback.answer()
        return

    text = f"🎯 <b>{title}</b>\n\n"
    current_clan = None
    for target in targets:
        enemy_clan = str(target["enemy_clan"])
        if enemy_clan != current_clan:
            current_clan = enemy_clan
            text += f"\n⚔️ <b>{escape(enemy_clan)}</b>\n"
        class_name = str(target["character_class"])
        text += (
            f"• <b>{escape(str(target['nickname']))}</b>"
            f" — {escape(CLASS_NAMES.get(class_name, class_name))}\n"
        )

    await callback.message.edit_text(
        text,
        reply_markup=targets_keyboard(targets),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("target:"))
async def target_selected(callback: CallbackQuery) -> None:
    if callback.message is None or not callback.data:
        await callback.answer("Повідомлення недоступне.", show_alert=True)
        return
    target_id = callback.data.partition(":")[2]
    try:
        targets = await get_targets()
    except Exception:
        await report_error(callback)
        return
    target = next(
        (item for item in targets if str(item.get("id")) == target_id),
        None,
    )
    if not target:
        await callback.answer("Ціль не знайдена.", show_alert=True)
        return
    await callback.message.answer(
        escape(f"/target {target.get('nickname', 'Unknown')}")
    )
    await callback.answer()

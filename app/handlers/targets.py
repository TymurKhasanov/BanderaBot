from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from app.keyboards.targets import (
    targets_keyboard,
    targets_rosters_keyboard,
)
from app.services.targets import (
    get_roster_targets,
    get_rosters_with_targets,
    get_targets,
)


router = Router()


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


@router.message(F.text == "🎯 Цілі")
async def targets_menu(message: Message):

    try:
        rosters = get_rosters_with_targets()

    except Exception as e:
        await message.answer(
            "❌ Не вдалося отримати цілі.\n\n"
            f"Помилка: {e}"
        )
        return

    if not rosters:
        await message.answer(
            "🎯 Цілі не знайдено."
        )
        return

    await message.answer(
        "🎯 <b>Оберіть команду</b>",
        reply_markup=targets_rosters_keyboard(rosters),
    )


@router.callback_query(F.data == "targets")
async def targets_back(callback: CallbackQuery):

    try:
        rosters = get_rosters_with_targets()

    except Exception:
        await callback.answer(
            "Не вдалося отримати цілі.",
            show_alert=True,
        )
        return

    if not rosters:
        await callback.answer(
            "Цілі не знайдено.",
            show_alert=True,
        )
        return

    await callback.message.edit_text(
        "🎯 <b>Оберіть команду</b>",
        reply_markup=targets_rosters_keyboard(rosters),
    )

    await callback.answer()


@router.callback_query(F.data.startswith("targets:roster:"))
async def roster_selected(callback: CallbackQuery):

    _, _, roster_id = callback.data.split(":", 2)

    try:
        roster = get_roster_targets(roster_id)

    except Exception:
        await callback.answer(
            "Не вдалося отримати цілі.",
            show_alert=True,
        )
        return

    if not roster:
        await callback.answer(
            "Команду не знайдено.",
            show_alert=True,
        )
        return

    targets = roster["targets"]

    if not targets:
        await callback.message.edit_text(
            f"🎯 <b>{roster['name']}</b>\n\n"
            "Цілей немає.",
        )
        await callback.answer()
        return

    targets.sort(
        key=lambda target: (
            target["enemy_clan"].lower(),
            target["pack_kind"].lower(),
            target["nickname"].lower(),
        )
    )

    text = f"🎯 <b>{roster['name']}</b>\n\n"

    current_clan = None
    current_pack_kind = None

    for target in targets:

        enemy_clan = target["enemy_clan"]
        pack_kind = target["pack_kind"]

        if enemy_clan != current_clan:
            current_clan = enemy_clan
            current_pack_kind = None

            text += (
                f"\n⚔️ <b>{enemy_clan}</b>\n"
            )

        if pack_kind != current_pack_kind:
            current_pack_kind = pack_kind

            text += (
                f"\n<b>{pack_kind}</b>\n"
            )

        character_class = CLASS_NAMES.get(
            target["character_class"],
            target["character_class"],
        )

        text += (
            f"• <b>{target['nickname']}</b>"
            f" — {character_class}\n"
        )

    await callback.message.edit_text(
        text,
        reply_markup=targets_keyboard(
            targets,
            roster_id,
        ),
    )

    await callback.answer()


@router.callback_query(F.data.startswith("target:"))
async def target_selected(callback: CallbackQuery):

    _, target_id = callback.data.split(":", 1)

    try:
        targets = get_targets()

    except Exception:
        await callback.answer(
            "Не вдалося отримати ціль.",
            show_alert=True,
        )
        return

    target = next(
        (
            target
            for target in targets
            if str(target.get("id")) == target_id
        ),
        None,
    )

    if not target:
        await callback.answer(
            "Ціль не знайдена.",
            show_alert=True,
        )
        return

    nickname = target.get("nickname")

    await callback.message.answer(
        f"/target {nickname}"
    )

    await callback.answer()
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

from app.keyboards.main import main_keyboard
from app.keyboards.dcp import dcp_keyboard
from app.keyboards.dcp_rosters import rosters_keyboard
from app.services.dcp_api import dcp_api

router = Router()


CLASS_ICONS = {
    # Archers
    "HAWKEYE": "🏹",
    "SILVER_RANGER": "🏹",
    "PHANTOM_RANGER": "🏹",

    # Daggers
    "TREASURE_HUNTER": "🗡️",
    "PLAINS_WALKER": "🗡️",
    "ABYSS_WALKER": "🗡️",

    # Tanks
    "PALADIN": "🛡️",
    "DARK_AVENGER": "🛡️",
    "TEMPLE_KNIGHT": "🛡️",
    "SHILLIEN_KNIGHT": "🛡️",

    # Warriors
    "GLADIATOR": "⚔️",
    "WARLORD": "⚔️",
    "DESTROYER": "⚔️",
    "TYRANT": "⚔️",

    # Mages
    "SORCERER": "🪄",
    "SPELLSINGER": "🪄",
    "SPELLHOWLER": "🪄",
    "NECROMANCER": "🪄",

    # Healers
    "BISHOP": "❤️",
    "CARDINAL": "❤️",

    # Buffers / Supports
    "PROPHET": "✨",
    "ELDER": "✨",
    "SHILLIEN_ELDER": "✨",
    "SWORDSINGER": "🎵",
    "BLADEDANCER": "💃",

    # Summoners
    "WARLOCK": "🐺",
    "ELEMENTAL_SUMMONER": "🐺",
    "PHANTOM_SUMMONER": "🐺",
}


@router.message(F.text == "📊 ДЦП")
async def dcp_menu(message: Message):
    await message.answer(
        "📊 <b>Меню ДЦП</b>\n\nОберіть потрібний розділ:",
        reply_markup=dcp_keyboard,
    )


@router.message(F.text == "👥 Ростери")
async def rosters(message: Message):
    try:
        rosters = dcp_api.get_rosters()

        if not rosters:
            await message.answer("Ростерів не знайдено.")
            return

        await message.answer(
            "👥 <b>Оберіть ростер</b>",
            reply_markup=rosters_keyboard(rosters),
        )

    except Exception as e:
        await message.answer(
            f"Помилка при отриманні ростерів:\n{e}"
        )


@router.callback_query(F.data.startswith("roster:"))
async def roster_info(callback: CallbackQuery):
    try:
        roster_id = callback.data.split(":")[1]

        rosters = dcp_api.get_rosters()

        roster = next(
            (r for r in rosters if str(r["id"]) == roster_id),
            None,
        )

        if roster is None:
            await callback.answer(
                "Ростер не знайдено",
                show_alert=True,
            )
            return

        members = roster.get("members", [])

        text = f"👥 <b>{roster['name']}</b>\n\n"

        if not members:
            text += "Учасників немає."
        else:
            for index, member in enumerate(members[:12], start=1):
                nickname = member["nickname"]
                class_name = member["className"]
                level = member["level"]

                icon = CLASS_ICONS.get(class_name, "⚔️")
                pretty_name = class_name.replace("_", " ").title()

                text += (
                    f"{index}. {icon} <b>{nickname}</b>\n"
                    f"   {pretty_name} | Lv.{level}\n"
                )

            if len(members) > 12:
                text += f"\n... ще {len(members) - 12} учасників"

        await callback.message.edit_text(text)

        await callback.answer()

    except Exception as e:
        await callback.answer(
            str(e),
            show_alert=True,
        )


@router.message(F.text == "💰 Баланс")
async def balance(message: Message):
    await message.answer(
        "🚧 Функція балансу буде реалізована пізніше."
    )


@router.message(F.text == "⬅️ Назад")
async def back_to_main(message: Message):
    await message.answer(
        "Головне меню",
        reply_markup=main_keyboard,
    )
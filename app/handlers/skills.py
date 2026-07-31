from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from app.keyboards.skills import (
    categories_keyboard,
    professions_keyboard,
    races_keyboard,
    skill_keyboard,
    skill_types_keyboard,
    skills_keyboard,
)
from app.services.wiki_classes import get_classes
from app.services.wiki_skills import get_skills

router = Router()

ACTIVE_CATEGORIES = [
    "Physical",
    "Buff",
    "Debuff",
    "Toggle",
    "Special",
    "Item",
    "Equipment",
    "Ability",
    "Additional",
]

RACE_TITLES = {
    "human": "👤 Human",
    "elf": "🧝 Elf",
    "dark_elf": "🌑 Dark Elf",
    "orc": "💪 Orc",
    "dwarf": "🔨 Dwarf",
}


@router.message(F.text == "⚔️ Skills")
async def skills_menu(message: Message):
    await message.answer(
        "⚔️ <b>Оберіть расу</b>",
        reply_markup=races_keyboard(),
    )


@router.callback_query(F.data == "skills")
async def skills_back(callback: CallbackQuery):
    await callback.message.edit_text(
        "⚔️ <b>Оберіть расу</b>",
        reply_markup=races_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("race:"))
async def race_selected(callback: CallbackQuery):
    _, race = callback.data.split(":", 1)

    classes = get_classes()

    await callback.message.edit_text(
        f"{RACE_TITLES[race]}\n\n<b>Оберіть професію</b>",
        reply_markup=professions_keyboard(
            race,
            classes[race],
        ),
    )

    await callback.answer()


@router.callback_query(F.data.startswith("class:"))
async def class_selected(callback: CallbackQuery):
    _, race, class_slug = callback.data.split(":", 2)

    # загрузит из JSON или скачает один раз
    get_skills(class_slug)

    await callback.message.edit_text(
        "⚔️ <b>Оберіть тип навичок</b>",
        reply_markup=skill_types_keyboard(
            race,
            class_slug,
        ),
    )

    await callback.answer()


@router.callback_query(F.data.startswith("type:"))
async def type_selected(callback: CallbackQuery):
    _, race, class_slug, skill_type = callback.data.split(":", 3)

    skills = get_skills(class_slug)

    if skill_type == "active":

        categories = [
            category
            for category in ACTIVE_CATEGORIES
            if category in skills
        ]

        await callback.message.edit_text(
            "🟢 <b>Active Skills</b>\n\nОберіть категорію:",
            reply_markup=categories_keyboard(
                categories,
                race,
                class_slug,
            ),
        )

    else:

        await callback.message.edit_text(
            "🛡 <b>Passive Skills</b>\n\nОберіть навичку:",
            reply_markup=skills_keyboard(
                skills.get("Passive", []),
                race,
                class_slug,
                "Passive",
            ),
        )

    await callback.answer()


@router.callback_query(F.data.startswith("cat:"))
async def category_selected(callback: CallbackQuery):
    _, race, class_slug, category = callback.data.split(":", 3)

    skills = get_skills(class_slug)

    await callback.message.edit_text(
        f"📚 <b>{category}</b>\n\nОберіть навичку:",
        reply_markup=skills_keyboard(
            skills[category],
            race,
            class_slug,
            category,
        ),
    )

    await callback.answer()


@router.callback_query(F.data.startswith("skill:"))
async def skill_selected(callback: CallbackQuery):
    _, race, class_slug, category, skill_slug = callback.data.split(":", 4)

    skills = get_skills(class_slug)

    skill = next(
        (
            s
            for s in skills[category]
            if s["slug"] == skill_slug
        ),
        None,
    )

    if skill is None:
        await callback.answer(
            "Навичку не знайдено.",
            show_alert=True,
        )
        return

    text = (
        f"⚔️ <b>{skill['name']}</b>\n"
        f"📈 <b>{skill['level']}</b>\n\n"
        f"{skill['description']}"
    )

    await callback.message.edit_text(
        text,
        reply_markup=skill_keyboard(
            skill,
            race,
            class_slug,
            category,
        ),
    )

    await callback.answer()
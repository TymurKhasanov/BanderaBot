from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def races_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👤 Human", callback_data="race:human")],
            [InlineKeyboardButton(text="🧝 Elf", callback_data="race:elf")],
            [InlineKeyboardButton(text="🌑 Dark Elf", callback_data="race:dark_elf")],
            [InlineKeyboardButton(text="💪 Orc", callback_data="race:orc")],
            [InlineKeyboardButton(text="🔨 Dwarf", callback_data="race:dwarf")],
        ]
    )


def professions_keyboard(race: str, professions: list) -> InlineKeyboardMarkup:
    keyboard = []

    for profession in professions:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=profession["name"],
                    callback_data=f"class:{race}:{profession['slug']}",
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="skills",
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def skill_types_keyboard(race: str, slug: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🟢 Active Skills",
                    callback_data=f"type:{race}:{slug}:active",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🛡 Passive Skills",
                    callback_data=f"type:{race}:{slug}:passive",
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data=f"race:{race}",
                )
            ],
        ]
    )


def categories_keyboard(categories: list, race: str, slug: str) -> InlineKeyboardMarkup:
    icons = {
        "Physical": "⚔️",
        "Buff": "✨",
        "Debuff": "☠️",
        "Toggle": "🔄",
        "Passive": "🛡",
        "Special": "⭐",
        "Item": "🎒",
        "Equipment": "🗡",
        "Ability": "💎",
        "Additional": "➕",
    }

    keyboard = []

    for category in categories:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{icons.get(category, '📂')} {category}",
                    callback_data=f"cat:{race}:{slug}:{category}",
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=f"type:{race}:{slug}:active",
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def skills_keyboard(
    skills: list,
    race: str,
    slug: str,
    category: str,
) -> InlineKeyboardMarkup:
    keyboard = []

    for skill in skills:
        level = f" ({skill['level']})" if skill["level"] else ""

        callback = f"skill:{race}:{slug}:{category}:{skill['slug']}"

        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{skill['name']}{level}",
                    callback_data=callback,
                )
            ]
        )

    if category == "Passive":
        back = f"type:{race}:{slug}:passive"
    else:
        # Назад к списку категорий активных навыков
        back = f"type:{race}:{slug}:active"

    keyboard.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=back,
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def skill_keyboard(
    skill: dict,
    race: str,
    slug: str,
    category: str,
) -> InlineKeyboardMarkup:
    if category == "Passive":
        back = f"type:{race}:{slug}:passive"
    else:
        # Назад к списку навыков выбранной категории
        back = f"cat:{race}:{slug}:{category}"

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🌐 Відкрити Wiki",
                    url=skill["url"],
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ До списку",
                    callback_data=back,
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠 До рас",
                    callback_data="skills",
                )
            ],
        ]
    )
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


def categories_keyboard(
    categories: list,
    race: str,
    slug: str,
    skill_type: str,
) -> InlineKeyboardMarkup:
    icons = {
        "Physical": "⚔️",
        "Magical": "🔮",
        "Buff": "✨",
        "Debuff": "☠️",
        "Toggle": "🔄",
        "Item": "🎒",
        "Equipment": "🗡",
        "Ability": "💎",
        "Additional": "➕",
        "Special": "⭐",
    }

    keyboard = []

    for category in categories:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{icons.get(category, '📂')} {category}",
                    callback_data=f"cat:{race}:{slug}:{skill_type}:{category}",
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=f"class:{race}:{slug}",
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def skills_keyboard(
    skills: list,
    race: str,
    slug: str,
    skill_type: str,
    category: str,
) -> InlineKeyboardMarkup:
    keyboard = []

    for skill in skills:
        level = f" ({skill['level']})" if skill["level"] else ""

        callback = f"skill:{race}:{slug}:{skill['slug']}"

        print(len(callback), callback)

        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{skill['name']}{level}",
                    callback_data=callback,
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=f"type:{race}:{slug}:{skill_type}",
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def skill_keyboard(
    skill: dict,
    race: str,
    slug: str,
    skill_type: str,
    category: str,
) -> InlineKeyboardMarkup:
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
                    callback_data=f"cat:{race}:{slug}:{skill_type}:{category}",
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
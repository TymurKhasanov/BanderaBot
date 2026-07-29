from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📅 Прайм"),
            KeyboardButton(text="👹 Епіки"),
        ],
        [
            KeyboardButton(text="📢 Оголошення"),
            KeyboardButton(text="📊 ДЦП"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Оберіть дію...",
)
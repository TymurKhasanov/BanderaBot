from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

dcp_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👥 Ростери"),
            KeyboardButton(text="💰 Баланс"),
        ],
        [
            KeyboardButton(text="⬅️ Назад"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Оберіть дію...",
)
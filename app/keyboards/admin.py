from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


admin_main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⚙️ Налаштування"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Оберіть дію...",
)
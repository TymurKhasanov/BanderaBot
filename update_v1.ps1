$root = "C:\Projects\BanderaBot"

function Write-PythonFile {
    param(
        [string]$Path,
        [string]$Content
    )

    $utf8 = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $utf8)

    Write-Host "Updated $Path"
}

# ==========================
# constants/texts.py
# ==========================

$texts = @'
START_MESSAGE = """
🇺🇦 <b>BanderaBot</b>

Вітаю!

Оберіть потрібний розділ.
"""

HELP_MESSAGE = """
📖 Доступні команди

/start — головне меню
/help — допомога
"""
'@

Write-PythonFile "$root\app\constants\texts.py" $texts

# ==========================
# keyboards/main.py
# ==========================

$keyboard = @'
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📅 Прайм"),
            KeyboardButton(text="👹 Епіки"),
        ],
        [
            KeyboardButton(text="📢 Оголошення"),
            KeyboardButton(text="⚙️ Налаштування"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Оберіть дію...",
)
'@

Write-PythonFile "$root\app\keyboards\main.py" $keyboard

# ==========================
# handlers/start.py
# ==========================

$start = @'
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.constants.texts import START_MESSAGE
from app.keyboards.main import main_keyboard

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        START_MESSAGE,
        reply_markup=main_keyboard,
        parse_mode="HTML",
    )
'@

Write-PythonFile "$root\app\handlers\start.py" $start

# ==========================
# handlers/help.py
# ==========================

$help = @'
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.constants.texts import HELP_MESSAGE

router = Router()


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        HELP_MESSAGE,
        parse_mode="HTML",
    )
'@

Write-PythonFile "$root\app\handlers\help.py" $help

# ==========================
# handlers/menu.py
# ==========================

$menu = @'
from aiogram import F, Router
from aiogram.types import Message

router = Router()


@router.message(F.text == "📅 Прайм")
async def prime(message: Message):
    await message.answer("📅 Розділ «Прайм» поки що в розробці.")


@router.message(F.text == "👹 Епіки")
async def epics(message: Message):
    await message.answer("👹 Розділ «Епіки» поки що в розробці.")


@router.message(F.text == "📢 Оголошення")
async def announcement(message: Message):
    await message.answer("📢 Розділ «Оголошення» поки що в розробці.")


@router.message(F.text == "⚙️ Налаштування")
async def settings(message: Message):
    await message.answer("⚙️ Розділ «Налаштування» поки що в розробці.")
'@

Write-PythonFile "$root\app\handlers\menu.py" $menu

# ==========================
# handlers/__init__.py
# ==========================

$init = @'
from .start import router as start_router
from .help import router as help_router
from .menu import router as menu_router

routers = [
    start_router,
    help_router,
    menu_router,
]
'@

Write-PythonFile "$root\app\handlers\__init__.py" $init

Write-Host ""
Write-Host "========================================="
Write-Host " BanderaBot updated to version 1"
Write-Host "========================================="
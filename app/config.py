from os import getenv
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set")

OWNER_ID = 137313739

DATABASE_PATH = "bandera_bot.db"

# DCP API
DCP_API_URL = getenv("DCP_API_URL")
DCP_LOGIN = getenv("DCP_LOGIN")
DCP_PASSWORD = getenv("DCP_PASSWORD")
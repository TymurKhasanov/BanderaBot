from aiogram import F, Router
from aiogram.types import Message

from app.services.dcp_api import dcp_api


router = Router()


@router.message(F.text == "🏷️ Лоти")
async def auctions(message: Message):

    try:
        auctions = dcp_api.get_auctions()
        rosters = dcp_api.get_rosters()

    except Exception as e:
        await message.answer(
            "❌ Не вдалося отримати лоти.\n\n"
            f"Помилка: {e}"
        )
        return

    # Только открытые аукционы
    auctions = [
        auction
        for auction in auctions
        if auction.get("status") == "OPEN"
    ]

    if not auctions:
        await message.answer(
            "🏷️ Відкритих лотів немає."
        )
        return

    # Словарь:
    # roster ID -> roster name
    roster_names = {
        str(roster["id"]): roster["name"]
        for roster in rosters
    }

    text = "🏷️ <b>Відкриті лоти</b>\n\n"

    for auction in auctions:

        lots = auction.get("lots", [])

        for lot in lots:

            title = lot.get("title", "Без назви")

            top_bidder = lot.get("topBidderName")
            roster_id = lot.get("topBidderRosterId")

            text += f"💎 <b>{title}</b>\n"

            if top_bidder and roster_id:
                roster_name = roster_names.get(
                    str(roster_id),
                    "Невідомий ростер",
                )

                text += (
                    f"👤 Топ бідер: {top_bidder}\n"
                    f"👥 Ростер: {roster_name}\n"
                )

            else:
                text += (
                    "👤 Топ бідер: Немає ставок\n"
                )

            text += "\n"

    await message.answer(text)
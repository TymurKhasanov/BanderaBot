import logging
from html import escape

from aiogram import F, Router
from aiogram.types import Message

from app.services.dcp_api import dcp_api


router = Router()
logger = logging.getLogger("banderabot")


@router.message(F.text == "🏷️ Лоти")
async def auctions(message: Message) -> None:
    try:
        items = await dcp_api.get_auctions()
        rosters = await dcp_api.get_rosters()
    except Exception:
        logger.exception("Failed to retrieve DCP auctions")
        await message.answer("❌ Сервіс лотів тимчасово недоступний.")
        return

    open_auctions = [
        auction
        for auction in items
        if auction.get("status") == "OPEN"
    ]
    if not open_auctions:
        await message.answer("🏷️ Відкритих лотів немає.")
        return

    roster_names = {
        str(roster.get("id")): str(roster.get("name", "Невідомий ростер"))
        for roster in rosters
    }
    lines = ["🏷️ <b>Відкриті лоти</b>", ""]
    for auction in open_auctions:
        for lot in auction.get("lots", []):
            title = escape(str(lot.get("title") or "Без назви"))
            lines.append(f"💎 <b>{title}</b>")
            top_bidder = lot.get("topBidderName")
            roster_id = lot.get("topBidderRosterId")
            if top_bidder and roster_id is not None:
                roster_name = roster_names.get(
                    str(roster_id),
                    "Невідомий ростер",
                )
                lines.extend(
                    (
                        f"👤 Топ бідер: {escape(str(top_bidder))}",
                        f"👥 Ростер: {escape(roster_name)}",
                    )
                )
            else:
                lines.append("👤 Топ бідер: Немає ставок")
            lines.append("")

    await message.answer("\n".join(lines).rstrip())

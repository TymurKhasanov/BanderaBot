import logging
import time

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

logger = logging.getLogger("banderabot")


class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        start = time.perf_counter()

        result = await handler(event, data)

        elapsed = (time.perf_counter() - start) * 1000

        if isinstance(event, Message):
            logger.info(
                "✅ MESSAGE | %s (@%s | %s) | %r | %.1f ms",
                event.from_user.full_name,
                event.from_user.username or "-",
                event.from_user.id,
                event.text,
                elapsed,
            )

        elif isinstance(event, CallbackQuery):
            logger.info(
                "✅ CALLBACK | %s (@%s | %s) | %s | %.1f ms",
                event.from_user.full_name,
                event.from_user.username or "-",
                event.from_user.id,
                event.data,
                elapsed,
            )

        return result
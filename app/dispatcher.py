import logging

from aiogram import Dispatcher
from aiogram.types import Update

logger = logging.getLogger("banderabot")


class BanderaDispatcher(Dispatcher):

    async def _process_update(self, bot, update: Update, **kwargs):
        handled = await super()._process_update(bot, update, **kwargs)

        if handled is True:
            return handled

        if update.message:
            m = update.message

            logger.warning(
                "\n"
                "================ NOT HANDLED ================\n"
                "Name      : %s\n"
                "Username  : @%s\n"
                "User ID   : %s\n"
                "Chat ID   : %s\n"
                "Chat Type : %s\n"
                "Message   : %r\n"
                "=============================================",
                m.from_user.full_name,
                m.from_user.username or "-",
                m.from_user.id,
                m.chat.id,
                m.chat.type,
                m.text,
            )

        elif update.callback_query:
            c = update.callback_query

            logger.warning(
                "\n"
                "============= NOT HANDLED CALLBACK ===========\n"
                "Name      : %s\n"
                "Username  : @%s\n"
                "User ID   : %s\n"
                "Chat ID   : %s\n"
                "Data      : %s\n"
                "==============================================",
                c.from_user.full_name,
                c.from_user.username or "-",
                c.from_user.id,
                c.message.chat.id if c.message else "-",
                c.data,
            )

        return handled
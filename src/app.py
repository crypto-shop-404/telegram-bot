import asyncio
import logging

import aiogram
from aiogram import executor

import handlers
import middlewares
import tasks
from services import db_api
from utils import notify_users


logger = logging.getLogger(__name__)


async def set_default_commands(dispatcher: aiogram.Dispatcher):
    await dispatcher.bot.set_my_commands(
        [
            aiogram.types.BotCommand("start", "Start bot"),
            aiogram.types.BotCommand('cancel', 'Cancel Command'),
        ]
    )


async def on_startup(dispatcher):
    tasks.setup_tasks()
    db_api.setup_database()
    middlewares.setup_middlewares(dispatcher)
    await set_default_commands(dispatcher)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    try:
        executor.start_polling(handlers.dp, on_startup=on_startup, skip_updates=True)
    except RuntimeError as e:
        logger.critical("Error during bot starting!")
        asyncio.run(
            notify_admins.notify_admins(
                (f"❗ Error During Operation ❗\n"
                 f"{e}\n\n❗"
                 f" The bot will restart automatically.")
            )
        )

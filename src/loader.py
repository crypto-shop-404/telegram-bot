import aiogram
import apscheduler.schedulers.asyncio
import tzlocal
from aiogram.contrib.fsm_storage import memory
from apscheduler import schedulers

import config


bot = aiogram.Bot(token=config.AppSettings().bot_token, parse_mode="HTML")
dp = aiogram.Dispatcher(bot, storage=memory.MemoryStorage())
scheduler = schedulers.asyncio.AsyncIOScheduler(timezone=str(tzlocal.get_localzone()))

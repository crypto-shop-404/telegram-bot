import aiogram.types
from aiogram import filters

import config


class IsUserAdmin(filters.BoundFilter):
    async def check(self, update: aiogram.types.Update) -> bool:
        if isinstance(update, (aiogram.types.Message, aiogram.types.CallbackQuery)):
            return update.from_user.id in config.AppSettings().admins_id

import aiogram.types
from aiogram import filters

from services import db_api
from services.db_api import queries


class IsUserInDB(filters.BoundFilter):
    def __init__(self, show_alert: bool = True):
        self.__show_alert = show_alert

    async def check(self, update: aiogram.types.Message | aiogram.types.CallbackQuery) -> bool:
        with db_api.create_session() as session:
            is_user_exists = queries.check_is_user_exists(session, update.from_user.id)
            if not is_user_exists and self.__show_alert:
                await update.answer("❌ You aren't in the database! Enter /start to register")
            return is_user_exists

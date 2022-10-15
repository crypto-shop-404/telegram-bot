import aiogram.types

import responses.profile
from loader import dp
from aiogram import filters

from services import db_api
from services.db_api import queries


@dp.message_handler(filters.Text('📱 Profile'))
async def profile(message: aiogram.types.Message):
    with db_api.create_session() as session:
        user = queries.get_user(session, telegram_id=message.from_user.id)
        queries.get_purchases(session, message.from_user.id)
        await responses.profile.ProfileResponse(
            message, user.id, user.username,
            queries.count_user_purchases(session, user.id),
            queries.get_user_orders_amount(session, user.id),
            queries.get_purchases(session, user.id, limit=10)
        )

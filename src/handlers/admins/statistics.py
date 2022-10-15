import aiogram
from aiogram import filters

import responses.statistics
from common import models
from filters import is_user_in_db, is_admin
from loader import dp
from services import db_api
from services.db_api import queries


@dp.message_handler(filters.Text('📊 Statistics'), is_user_in_db.IsUserInDB(), is_admin.IsUserAdmin())
async def statistics(message: aiogram.types.Message):
    await responses.statistics.StatisticsMenuResponse(message)


@dp.message_handler(filters.Text('📊 General'), is_user_in_db.IsUserInDB(), is_admin.IsUserAdmin())
async def general_statistics(message: aiogram.types.Message):
    with db_api.create_session() as session:
        buyers = []
        for telegram_id, username, quantity, amount in queries.get_buyers(session):
            buyer: models.Buyer = {
                'telegram_id': telegram_id, 'username': username,
                'purchase_number': quantity, 'orders_amount': amount
            }
            buyers.append(buyer)

        await responses.statistics.StatisticsResponse(
            message,
            queries.count_users(session),
            queries.get_total_orders_amount(session),
            queries.count_purchases(session),
            queries.get_purchases(session),
            buyers
        )


@dp.message_handler(filters.Text('📆 Daily'), is_user_in_db.IsUserInDB(), is_admin.IsUserAdmin())
async def daily_statistics(message: aiogram.types.Message):
    await message.answer('🚧 Under Development')

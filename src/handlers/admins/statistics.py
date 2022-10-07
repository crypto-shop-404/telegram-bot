import aiogram

import responses.statistics
from loader import dp
from aiogram import filters
from filters import is_user_in_db, is_admin
from services import db_api
from services.db_api import queries


@dp.message_handler(filters.Text('📊 Statistics'), is_user_in_db.IsUserInDB(), is_admin.IsUserAdmin())
async def statistics(message: aiogram.types.Message):
    await responses.statistics.StatisticsMenuResponse(message)


@dp.message_handler(filters.Text('📊 General'), is_user_in_db.IsUserInDB(), is_admin.IsUserAdmin())
async def general_statistics(message: aiogram.types.Message):
    with db_api.create_session() as session:
        await responses.statistics.StatisticsResponse(
            message,
            queries.count_users(session),
            queries.get_total_orders_amount(session),
            queries.count_sold_product_units(session),
            queries.get_products_sold_units_quantity(session),
            queries.get_buyers(session)
    )


@dp.message_handler(filters.Text('📆 Daily'), is_user_in_db.IsUserInDB(), is_admin.IsUserAdmin())
async def daily_statistics(message: aiogram.types.Message):
    await message.answer('🚧 Under Development')

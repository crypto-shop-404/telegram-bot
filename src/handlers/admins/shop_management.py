import aiogram.types

import responses.shop_management
from aiogram import filters
from loader import dp
from filters import is_admin, is_user_in_db


@dp.message_handler(filters.Text('📦 All Products'), is_user_in_db.IsUserInDB(), is_admin.IsUserAdmin())
async def shop_management(message: aiogram.types.Message):
    await responses.shop_management.ShopManagementResponse(message)

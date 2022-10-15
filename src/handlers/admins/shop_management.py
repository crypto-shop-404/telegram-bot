import aiogram.types
from aiogram import filters

import responses.shop_management
from filters import is_admin
from loader import dp


@dp.message_handler(filters.Text('📦 All Products'), is_admin.IsUserAdmin())
async def shop_management(message: aiogram.types.Message):
    await responses.shop_management.ShopManagementResponse(message)

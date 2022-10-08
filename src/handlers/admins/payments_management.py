import aiogram.types

import responses.payments_management
from loader import dp
from aiogram import filters
from filters import is_user_in_db, is_admin


@dp.message_handler(filters.Text('💳 Payment Management'), is_user_in_db.IsUserInDB(), is_admin.IsUserAdmin())
async def payments_management(message: aiogram.types.Message):
    await responses.payments_management.PaymentsManagementResponse(message)

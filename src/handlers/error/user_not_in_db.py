import aiogram.types

from loader import dp
import exceptions


@dp.errors_handler(exception=exceptions.UserNotInDatabase)
async def user_not_in_db_error(update: aiogram.types.Update, exception: exceptions.UserNotInDatabase):
    await update.message.answer("❌ You aren't in the database! Enter /start to register")
    return True

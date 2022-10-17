import aiogram.types

from loader import dp
import exceptions


@dp.errors_handler(exception=exceptions.UserNotInDatabase)
async def user_not_in_db_error(update: aiogram.types.Update, _: exceptions.UserNotInDatabase):
    text = "❌ You aren't in the database! Enter /start to register"
    if update.callback_query is not None:
        await update.callback_query.message.answer(text)
    elif update.message is not None:
        await update.message.answer(text)
    return True

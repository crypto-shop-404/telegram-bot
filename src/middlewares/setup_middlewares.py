import aiogram.dispatcher

from middlewares import banned_user_middleware


def setup_middlewares(dp: aiogram.Dispatcher):
    dp.setup_middleware(banned_user_middleware.BannedUserMiddleware())

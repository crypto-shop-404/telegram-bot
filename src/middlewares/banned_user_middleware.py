import aiogram.types
from aiogram.dispatcher import middlewares, handler
from services.db_api import queries
from services import db_api


class BannedUserMiddleware(middlewares.BaseMiddleware):
    @staticmethod
    async def on_pre_process_update(update: aiogram.types.Update, _):
        user_id = None
        if update.message:
            user_id = update.message.from_user.id
        elif update.callback_query:
            user_id = update.callback_query.from_user.id
        if user_id is not None:
            with db_api.create_session() as session:
                if queries.check_is_user_banned(session, user_id):
                    raise handler.CancelHandler()

import aiogram.types
from aiogram import types
from aiogram.dispatcher import filters

import responses.main_menu
import responses.start
from loader import dp
from services import db_api, notifications
from services.db_api import queries


@dp.message_handler(filters.Text('✅ Accept'))
async def accept_rules(message: aiogram.types.Message):
    with db_api.create_session() as session:
        queries.add_user(
            session, message.from_user.id, message.from_user.username.lower()
        )
        await responses.start.NewUserResponse(message)
        await responses.main_menu.UserMainMenuResponse(message)
        await notifications.NewUserNotification(message.from_user.id, message.from_user.username).send()


@dp.message_handler(filters.CommandStart())
async def start(message: types.Message):
    with db_api.create_session() as session:
        if queries.check_is_user_exists(session, message.from_user.id):
            await responses.start.UserExistsResponse(message)
            await responses.main_menu.UserMainMenuResponse(message)
        else:
            await responses.start.RulesResponse(message)

import typing

import aiogram.types

import config
import loader


KeyboardMarkup: typing.TypeAlias = aiogram.types.InlineKeyboardMarkup | aiogram.types.ReplyKeyboardMarkup


async def notify_admins(message: str, keyboard: KeyboardMarkup = None):
    for admin_id in config.AppSettings.admins_id:
        await loader.bot.send_message(admin_id, message, reply_markup=keyboard)


async def notify_user(user_id: int, message: str, keyboard: KeyboardMarkup = None):
    await loader.bot.send_message(user_id, message, reply_markup=keyboard)

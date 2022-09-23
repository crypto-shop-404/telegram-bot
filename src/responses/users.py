import datetime

import aiogram.types

from keyboards.inline import users_keyboard, common_keybords, callback_factories
from responses import base
from services.db_api import schemas


class UsersResponse(base.BaseResponse):
    def __init__(self, update: aiogram.types.CallbackQuery | aiogram.types.Message,
                 users: list[schemas.User], total_balance: float, users_filter: str = '',
                 page: int = 0, page_size: int = 10, callback_data: dict[str, str] = None):
        self.__update = update
        self.__keyboard = users_keyboard.UsersKeyboard(users, page, page_size, users_filter, callback_data)
        self.__users_quantity = len(users)
        self.__total_balance = total_balance
        self.__page = page
        self.__page_size = page_size

    async def _send_response(self):
        text = (
            f"Total Users: {self.__users_quantity}\n"
            f"Total Balances in User's profiles: ${self.__total_balance or 0.0}"
        )
        if isinstance(self.__update, aiogram.types.CallbackQuery):
            await self.__update.answer()
            await self.__update.message.edit_text(text, reply_markup=self.__keyboard)
        elif isinstance(self.__update, aiogram.types.Message):
            await self.__update.answer(text, reply_markup=self.__keyboard)


class UserResponse(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery, user: schemas.User,
                 number_of_orders: int, callback_data: dict[str, str] = None):
        self.__query = query
        self.__user = user
        self.__number_of_orders = number_of_orders
        if callback_data is None:
            callback_data = {
                '@': 'users', 'filter': '', 'page': '0',
                'id': user.id, 'action': 'manage', 'is_confirmed': ''
            }
        else:
            callback_data['is_confirmed'] = ''
        self.__keyboard = users_keyboard.UserKeyboard(user.id, user.is_banned, callback_data=callback_data)

    async def _send_response(self):
        text = (
                f'<b>User ID</b>: {self.__user.telegram_id}\n' +
                (f'<b>Username</b>: @{self.__user.username}\n' if self.__user.username else '') +
                f'<b>Registration Date</b>: {self.__user.created_at.date()}\n'
                f'<b>Number of orders</b>: {self.__number_of_orders}\n'
                f'<b>Balance</b>: ${self.__user.balance}\n\n'
                f'<b>Status</b>: {"banned" if self.__user.is_banned else "not banned"}'
        )
        await self.__query.answer()
        await self.__query.message.edit_text(text, reply_markup=self.__keyboard, parse_mode='HTML')


class SearchUserResponse(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery):
        self.__query = query

    async def _send_response(self):
        text = '🆔 Enter usernames or ids'
        await self.__query.answer()
        await self.__query.message.edit_text(text)


class FoundUsersResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message):
        self.__message = message

    async def _send_response(self) -> aiogram.types.Message:
        return await self.__message.answer(f'🔡 Found users with these usernames and ids: {self.__message.text}')


class BanUserAlertResponse(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery, user: schemas.User, callback_data: dict[str, str]):
        self.__query = query
        self.__user = user
        self.__keyboard = common_keybords.ConfirmationKeyboard(
            callback_factories.UserCallbackFactories(), **callback_data
        )

    async def _send_response(self):
        await self.__query.answer()
        await self.__query.message.edit_text(
            f'Are you sure you want to ban '
            f'{self.__user.username if self.__user.username is not None else "user"} '
            f'with {self.__user.telegram_id}?',
            reply_markup=self.__keyboard
        )


class UnbanUserAlertResponse(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery, user: schemas.User, callback_data: dict[str, str]):
        self.__query = query
        self.__user = user
        self.__keyboard = common_keybords.ConfirmationKeyboard(
            callback_factories.UserCallbackFactories(), **callback_data
        )

    async def _send_response(self):
        await self.__query.answer()
        await self.__query.message.edit_text(
            f'Are you sure you want to unban '
            f'{self.__user.username if self.__user.username is not None else "user"} '
            f'with {self.__user.telegram_id}?',
            reply_markup=self.__keyboard
        )


class DeleteUserAlert(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery, user: schemas.User, callback_data: dict[str, str]):
        self.__query = query
        self.__user = user
        self.__keyboard = common_keybords.ConfirmationKeyboard(
            callback_factories.UserCallbackFactories(), **callback_data
        )

    async def _send_response(self):
        text = (
            f'This user has ${self.__user.balance} left. Are you sure you want to delete this user?'
        )
        await self.__query.answer()
        await self.__query.message.edit_text(text, reply_markup=self.__keyboard)


class SuccessUserRemovalResponse(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery,  user: schemas.User):
        self.__user = user
        self.__query = query

    async def _send_response(self) -> aiogram.types.Message:
        text = (f'✅ Deleted {self.__user.username or "user"} with {self.__user.telegram_id}'
                f' and previous balance of {self.__user.balance}')
        await self.__query.answer()
        return await self.__query.message.edit_text(text=text)


class EditBalanceAlertResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message, user: schemas.User,
                 new_balance: str, callback_data: dict[str, str]):
        self.__message = message
        self.__user = user
        self.__new_balance = new_balance
        callback_data['balance'] = new_balance
        self.__keyboard = common_keybords.ConfirmationKeyboard(
            callback_factories.EditBalanceCallbackFactories(), **callback_data
        )

    async def _send_response(self):
        text = (f'Are you sure you want to change the balance of {self.__user.username or "user"}'
                f' with {self.__user.telegram_id} from ${self.__user.balance} to ${self.__new_balance}?')
        await self.__message.answer(text, reply_markup=self.__keyboard)


class NewBalanceResponse(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery):
        self.__query = query

    async def _send_response(self):
        text = '💱 Please type the amount for the new balance:'
        await self.__query.answer()
        await self.__query.message.edit_text(text)


class IncorrectBalanceResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message):
        self.__message = message

    async def _send_response(self):
        await self.__message.answer('❌ Incorrect balance!')


class BalanceEditingReasonResponse(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
        self.__query = query
        self.__keyboard = users_keyboard.BalanceEditingReasonsKeyboard(
            int(callback_data['user_id']), float(callback_data['balance'])
        )

    async def _send_response(self):
        text = '❓ Enter the reason of change balance:'
        await self.__query.answer()
        await self.__query.message.edit_text(text, reply_markup=self.__keyboard)


class SuccessBalanceEditing(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery, user: schemas.User, new_balance: float, reason: str):
        self.__query = query
        self.__user = user
        self.__new_balance = new_balance
        self.__reason = reason

    async def _send_response(self):
        text = (
                f'Changed balance of {self.__user.username or "user"}'
                f' with {self.__user.telegram_id} from ${self.__user.balance} to ${self.__new_balance}\n'
                f'<code>Date: {datetime.date.today()}\n' +
                (f'Username: {self.__user.username}\n' if self.__user.username is not None else '') +
                f'ID: {self.__user.telegram_id}\n'
                f'Previous balance: {self.__user.balance}\n'
                f'New Balance: {self.__new_balance}\n'
                f'Reason: {self.__reason}</code>'
        )
        await self.__query.answer()
        await self.__query.message.answer(text, parse_mode='HTML')


class TopUpBalanceAlertResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message, user: schemas.User,
                 balance: str, callback_data: dict[str, str]):
        self.__message = message
        self.__user = user
        self.__balance = balance
        callback_data['balance_delta'] = balance
        self.__keyboard = common_keybords.ConfirmationKeyboard(
            callback_factories.TopUpCallbackFactories(), **callback_data
        )

    async def _send_response(self):
        text = (f'Are you sure you want to top-up the balance of {self.__user.username or "user"}'
                f' with {self.__user.telegram_id} for ${self.__balance}?')
        await self.__message.answer(text, reply_markup=self.__keyboard)


class BalanceRefillMethodResponse(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
        self.__query = query
        self.__keyboard = users_keyboard.BalanceRefillMethodsKeyboard(
            int(callback_data['user_id']), float(callback_data['balance_delta'])
        )

    async def _send_response(self):
        text = '❓ Enter the manual payment method the user paid:'
        await self.__query.answer()
        await self.__query.message.edit_text(text, reply_markup=self.__keyboard)


class SuccessBalanceRefillResponse(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery, user: schemas.User, balance_delta: float, method: str):
        self.__query = query
        self.__user = user
        self.__balance_delta = balance_delta
        self.__method = method

    async def _send_response(self):
        text = (
            f'Topped-up {self.__user.username or "user"} '
            f'with {self.__user.telegram_id} for ${self.__balance_delta}\n'
            f'<code>Date: {datetime.date.today()}\n' +
            (f'Username: {self.__user.username}\n' if self.__user.username is not None else '') +
            f'ID: {self.__user.telegram_id}\n'
            f'Topped Up amount: {self.__balance_delta}\n'
            f'Total Balance: {self.__user.balance}\n'
            f'Method of payment: {self.__method}</code>'
        )
        await self.__query.answer()
        await self.__query.message.answer(text)

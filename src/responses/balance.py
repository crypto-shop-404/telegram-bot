import contextlib

import aiogram.types

from keyboards.buttons import common_buttons
from keyboards.inline import balance_keyboards, payments_keyboards, callback_factories
from responses import base


class BalanceResponse(base.BaseResponse):

    def __init__(self, message: aiogram.types.Message, balance: float):
        self.__message = message
        self.__balance = balance
        self.__keyboard = balance_keyboards.TopUpBalanceKeyboard()

    async def _send_response(self):
        await self.__message.answer(
            f'⚖️ You current balance: ${self.__balance}\n'
            f'Do you want top up it?', reply_markup=self.__keyboard
        )


class BalanceAmountResponse(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery):
        self.__query = query

    async def _send_response(self):
        await self.__query.answer()
        await self.__query.message.edit_text('🔢 Enter amount')


class IncorrectBalanceAmountResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message):
        self.__message = message

    async def _send_response(self):
        await self.__message.answer('💯 Incorrect balance amount!')


class PaymentMethodResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message, callback_data: dict[str: str],
                 crypto_payments: str = None):
        self.__message = message
        callback_data.pop('@')
        self.__keyboard = payments_keyboards.PaymentMethodsKeyboard(
            callback_data, callback_factories.TopUpBalanceCallbackFactory(),
            crypto_payments=crypto_payments
        )
        self.__keyboard.add(common_buttons.CloseButton())

    async def _send_response(self):
        await self.__message.answer('💲 Choose payment method', reply_markup=self.__keyboard)


class SuccessBalanceRefillResponse(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery, amount: float):
        self.__query = query
        self.__amount = amount

    async def _send_response(self):
        with contextlib.suppress(aiogram.exceptions.InvalidQueryID):
            await self.__query.answer()
        await self.__query.message.edit_text(f'✅ Balance was topped up by {self.__amount}')


class FailedBalanceRefillResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message):
        self.__message = message

    async def _send_response(self):
        await self.__message.edit_text('🚫 Balance refill failed')

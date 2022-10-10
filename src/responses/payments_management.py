import aiogram.types

import keyboards.inline.payments_management_keyboards
from keyboards import inline
from keyboards.reply import payments_management_keyboards
from responses import base


class PaymentsManagementResponse(base.BaseResponse):

    def __init__(self, message: aiogram.types.Message):
        self.__message = message
        self.__keyboard = payments_management_keyboards.PaymentsKeyboard()

    async def _send_response(self):
        await self.__message.answer('💳 Payment Management', reply_markup=self.__keyboard)


class CoinbaseManagementResponse(base.BaseResponse):
    def __init__(self, update: aiogram.types.Message | aiogram.types.CallbackQuery, is_valid: bool = None):
        self.__update = update
        self.__keyboard = inline.payments_management_keyboards.CoinbaseKeyboard()
        self.__is_valid = is_valid

    async def _send_response(self):
        text = '🌐 Coinbase\n'
        status = ''
        if self.__is_valid is not None:
            status = f'Status: {"✅ OK" if self.__is_valid else "❌ ERROR"}'
            text += status
        if isinstance(self.__update, aiogram.types.Message):
            await self.__update.answer(text, reply_markup=self.__keyboard)
        elif isinstance(self.__update, aiogram.types.CallbackQuery):
            await self.__update.answer()
            if status not in self.__update.message.text:
                await self.__update.message.edit_text(text, reply_markup=self.__keyboard)


class PaymentSystemIsValid(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery):
        self.__query = query

    async def _send_response(self):
        await CoinbaseManagementResponse(self.__query, True)


class PaymentSystemIsNotValid(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery):
        self.__query = query

    async def _send_response(self):
        await CoinbaseManagementResponse(self.__query, False)


class ChangeCoinbaseAPIKeyResponse(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery):
        self.__query = query

    async def _send_response(self):
        await self.__query.answer()
        await self.__query.message.edit_text('🔑 Enter api key')


class SuccessChangingPaymentsData(base.BaseResponse):
    def __init__(self, message: aiogram.types):
        self.__message = message

    async def _send_response(self):
        await self.__message.answer('✅ Success! Data has been changed.')

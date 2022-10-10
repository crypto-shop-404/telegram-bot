import aiogram.types

from responses import base
from keyboards.inline import payments_keyboards


class CoinbasePaymentLinkResponse(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery, amount: float,
                 quantity: int, payment_url: str):
        self.__query = query
        self.__amount = amount
        self.__quantity = quantity
        self.__keyboard = payments_keyboards.CoinbasePaymentKeyboard(payment_url)

    async def _send_response(self):
        await self.__query.answer()
        await self.__query.message.edit_text(
            "<b>Currency</b>: USD\n"
            f"<b>Quantity</b>: {self.__quantity}\n"
            f"<b>Amount: {self.__amount}</b>",
            reply_markup=self.__keyboard
        )


class FailedPurchaseResponse(base.BaseResponse):

    def __init__(self, message: aiogram.types.Message):
        self.__message = message

    async def _send_response(self):
        await self.__message.edit_text('🚫 Purchase failed')


class NotEnoughBalanceResponse(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery):
        self.__query = query

    async def _send_response(self):
        await self.__query.message.edit_text('⭕️ Not enough balance!')

import aiogram.types

from responses import base
from keyboards.reply import payments_management_keyboards


class PaymentsManagementResponse(base.BaseResponse):

    def __init__(self, message: aiogram.types.Message):
        self.__message = message
        self.__keyboard = payments_management_keyboards.PaymentsKeyboard()

    async def _send_response(self):
        await self.__message.answer('💳 Payment Management', reply_markup=self.__keyboard)

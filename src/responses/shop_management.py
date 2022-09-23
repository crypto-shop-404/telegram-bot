import aiogram.types

import keyboards.reply.shop_management_keyboards
from responses import base


class ShopManagementResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message):
        self.__message = message
        self.__keyboard = keyboards.reply.shop_management_keyboards.ShopManagementKeyboard()

    async def _send_response(self):
        await self.__message.answer('📦 All Products', reply_markup=self.__keyboard)

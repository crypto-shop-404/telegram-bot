import aiogram.types

from keyboards.reply import main_menu_keyboards
from responses import base


class AdminMainMenuResponse(base.BaseResponse):
    __slots__ = ('__message', '__keyboard')

    def __init__(self, message: aiogram.types.Message):
        self.__message = message
        self.__keyboard = main_menu_keyboards.AdminMainMenuKeyboard()

    async def _send_response(self) -> aiogram.types.Message:
        return await self.__message.answer(text='🔹 Main Menu 🔹', reply_markup=self.__keyboard)


class UserMainMenuResponse(base.BaseResponse):
    __slots__ = ('__message', '__keyboard')

    def __init__(self, message: aiogram.types.Message):
        self.__message = message
        self.__keyboard = main_menu_keyboards.UserMainMenuKeyboard()

    async def _send_response(self) -> aiogram.types.Message:
        return await self.__message.answer(text='🔹 Main Menu 🔹', reply_markup=self.__keyboard)

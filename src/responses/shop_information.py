import aiogram.types

from responses import base
from keyboards.reply import shop_information_keyboards


class ShopInformationResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message):
        self.__message = message
        self.__keyboard = shop_information_keyboards.ShopInformationKeyboard()

    async def _send_response(self):
        await self.__message.answer('🏪 Shop information', reply_markup=self.__keyboard)


class FAQResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message, faq: str):
        self.__message = message
        self.__faq = faq
        self.__keyboard = shop_information_keyboards.EditFAQKeyboard()

    async def _send_response(self):
        await self.__message.answer(self.__faq, reply_markup=self.__keyboard)


class RulesResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message, rules: str):
        self.__message = message
        self.__rules = rules
        self.__keyboard = shop_information_keyboards.EditRulesKeyboard()

    async def _send_response(self):
        await self.__message.answer(self.__rules, reply_markup=self.__keyboard)


class GreetingsResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message, greetings: str):
        self.__message = message
        self.__greetings = greetings
        self.__keyboard = shop_information_keyboards.EditGreetingsKeyboard()

    async def _send_response(self):
        await self.__message.answer(self.__greetings, reply_markup=self.__keyboard)


class ComebackMessageResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message, comeback_message: str):
        self.__message = message
        self.__comeback_message = comeback_message
        self.__keyboard = shop_information_keyboards.EditComebackMessageKeyboard()

    async def _send_response(self):
        await self.__message.answer(self.__comeback_message, reply_markup=self.__keyboard)


class EditShopInformationResponse(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery):
        self.__query = query

    async def _send_response(self):
        await self.__query.answer()
        await self.__query.message.edit_text('✏️ Enter a new value')


class SuccessShopInformationEditing(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message):
        self.__message = message

    async def _send_response(self):
        await self.__message.answer('✅ The value is changed')

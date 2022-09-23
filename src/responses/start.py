import aiogram.types

from responses import base
from keyboards.reply import rules_keyboards


class UserExistsResponse(base.BaseResponse):
    __slots__ = ('__message',)

    def __init__(self, message: aiogram.types.Message):
        self.__message = message

    async def _send_response(self) -> aiogram.types.Message:
        return await self.__message.answer('Comeback Message!')

    def __repr__(self):
        return f'{type(self).__name__}(message={self.__message})'


class NewUserResponse(base.BaseResponse):
    __slots__ = ('__message', '__markup', '__message_text')

    def __init__(self, message: aiogram.types.Message):
        self.__message = message
        self.__message_text = f'Hello {self.__message.from_user.full_name}!'

    async def _send_response(self) -> aiogram.types.Message:
        return await self.__message.answer(text=self.__message_text)

    def __repr__(self):
        return f'{type(self).__name__}(message={self.__message})'


class RulesResponse(base.BaseResponse):
    __slots__ = ('__message',)

    def __init__(self, message: aiogram.types.Message):
        self.__message = message

    async def _send_response(self) -> aiogram.types.Message:
        return await self.__message.answer('Rules', reply_markup=rules_keyboards.AcceptRulesKeyboard())

    def __repr__(self):
        return f'{type(self).__name__}(message={self.__message})'

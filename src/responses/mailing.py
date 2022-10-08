import aiogram.types

import keyboards.reply.mailing_keyboards
from responses import base


class MailingResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message):
        self.__message = message
        self.__keyboard = keyboards.reply.mailing_keyboards.MailingKeyboard()

    async def _send_response(self):
        await self.__message.answer(
            text='📧 Newsletter', reply_markup=self.__keyboard
        )


class CreateNewsletterResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message):
        self.__message = message

    async def _send_response(self) -> aiogram.types.Message:
        return await self.__message.answer(
            '✏️ Enter the text of your newsletter in the usual telegram format\n'
            'Or attach a photo, and specify the text in the description to the picture'
        )


class MailingStartResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message):
        self.__message = message

    async def _send_response(self) -> aiogram.types.Message:
        return await self.__message.answer('✅ The mailing has started')


class MailingFinishResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message, successful_newsletters: int,
                 unsuccessful_newsletters: int):
        self.__message = message
        self.__unsuccessful_newsletters = unsuccessful_newsletters
        self.__successful_newsletters = successful_newsletters

    async def _send_response(self) -> aiogram.types.Message:
        return await self.__message.answer(
            '✅ The newsletter is completed\n'
            f'Total sent: {self.__unsuccessful_newsletters + self.__successful_newsletters}\n\n'
            f'✅ Successful: {self.__successful_newsletters}\n'
            f'❌ Not sent: {self.__unsuccessful_newsletters}'
        )

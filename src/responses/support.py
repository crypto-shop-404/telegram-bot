import aiogram.types

from keyboards.reply import support_keybords
from responses import base
from services.db_api import schemas


class UserSupportMenuResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message):
        self.__message = message
        self.__keyboard = support_keybords.UserSupportKeyboard()

    async def _send_response(self):
        await self.__message.answer('👨‍💻 Support', reply_markup=self.__keyboard)


class AdminSupportMenuResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message):
        self.__message = message
        self.__keyboard = support_keybords.AdminSupportKeyboard()

    async def _send_response(self):
        await self.__message.answer('👨‍💻 Support', reply_markup=self.__keyboard)


class NewSupportSubjectResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message):
        self.__message = message

    async def _send_response(self):
        await self.__message.answer('🛟 Input support subject')


class SuccessAddingSupportSubjectResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message):
        self.__message = message

    async def _send_response(self):
        await self.__message.answer('✅ Ready')


class NewSupportRequestResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message, subjects: list[schemas.SupportSubject]):
        self.__message = message
        self.__keyboard = support_keybords.NewSupportRequestSubjectsKeyboard(subjects)

    async def _send_response(self):
        await self.__message.answer('📋 New Support Request', reply_markup=self.__keyboard)


class NewSupportRequestIssueResponse(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery):
        self.__query = query

    async def _send_response(self):
        await self.__query.answer()
        await self.__query.message.edit_text('📋 Describe your problem/question')


class SuccessAddingSupportRequestResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message, request_number: int):
        self.__message = message
        self.__request_number = request_number

    async def _send_response(self):
        await self.__message.answer((
            '✔️ Your support request has been sent\n\n'
            f'🆔 Request number: {self.__request_number}')
        )


class UserSupportRequestsResponse(base.BaseResponse):
    def __init__(self, update: aiogram.types.Message | aiogram.types.CallbackQuery,
                 support_requests: list[schemas.SupportRequest]):
        self.__update = update
        self.__keyboard = support_keybords.SupportRequestsKeyboard(support_requests, user_id=self.__update.from_user.id)

    async def _send_response(self):
        if isinstance(self.__update, aiogram.types.Message):
            await self.__update.answer('📚 My Support Requests', reply_markup=self.__keyboard)


class ClosedSupportRequestsResponse(base.BaseResponse):
    def __init__(self, update: aiogram.types.Message | aiogram.types.CallbackQuery,
                 support_requests: list[schemas.SupportRequest]):
        self.__update = update
        self.__keyboard = support_keybords.SupportRequestsKeyboard(
            support_requests, is_open=False
        )

    async def _send_response(self):
        if isinstance(self.__update, aiogram.types.Message):
            await self.__update.answer('📕 Closed Requests', reply_markup=self.__keyboard)
        elif isinstance(self.__update, aiogram.types.CallbackQuery):
            await self.__update.answer()
            await self.__update.message.edit_text('📕 Closed Requests', reply_markup=self.__keyboard)


class OpenSupportRequestsResponse(base.BaseResponse):
    def __init__(self, update: aiogram.types.Message | aiogram.types.CallbackQuery,
                 support_requests: list[schemas.SupportRequest]):
        self.__update = update
        self.__keyboard = support_keybords.SupportRequestsKeyboard(
            support_requests, is_open=True
        )

    async def _send_response(self):
        if isinstance(self.__update, aiogram.types.Message):
            await self.__update.answer('📗Active Requests', reply_markup=self.__keyboard)
        elif isinstance(self.__update, aiogram.types.CallbackQuery):
            await self.__update.answer()
            await self.__update.message.edit_text('📗Active Requests', reply_markup=self.__keyboard)


class SupportRequestResponse(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery, support_request: schemas.SupportRequest,
                 is_open: bool = None, user_id: int = None):
        self.__query = query
        self.__request = support_request
        self.__keyboard = support_keybords.SupportRequestMenuKeyboard(support_request.id, is_open, user_id)

    async def _send_response(self):
        await self.__query.answer()
        await self.__query.message.edit_text(
            (f'🆔 Request number: {self.__request.id}\n'
             '➖➖➖➖➖➖➖➖➖➖\n'
             f'📗 Request Subject: {self.__request.subject.name}\n'
             '📋 Description:\n'
             f'{self.__request.issue}\n'
             '➖➖➖➖➖➖➖➖➖➖\n'
             f'📱 Status: {"✅ Active" if self.__request.is_open else "❌ Closed"}' +
             (
                 '\n➖➖➖➖➖➖➖➖➖➖\n'
                 '📧 Answer:\n\n'
                 f'{self.__request.answer}' if not self.__request.is_open else ""
             )),
            reply_markup=self.__keyboard
        )


class AnswerSupportRequestResponse(base.BaseResponse):
    def __init__(self, query: aiogram.types.CallbackQuery):
        self.__query = query

    async def _send_response(self):
        await self.__query.answer()
        await self.__query.message.edit_text('✏️ Enter Answer')

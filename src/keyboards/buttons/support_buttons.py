import aiogram.types
from keyboards.inline import callback_factories


class ActiveSupportRequestsButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='📗 Active Requests')


class ClosedSupportRequestsButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='📕 Closed Requests')


class NewSupportSubjectButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='🆘 New Support Subject')


class NewSupportRequestButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='📋 New Support Request')


class UsersSupportsButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='📓 My Support Requests')


class NewSupportRequestSubjectButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, subject_id: int, subject_name: str):
        super().__init__(
            text=subject_name, callback_data=callback_factories.CreateSupportCallbackFactory().new(subject_id)
        )


class SupportRequestButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, is_open: bool | None, user_id: int | None, support_request_id: int, issue: str):
        super().__init__(
            f'#{support_request_id} {issue[:18] + ("..." if len(issue) > 18 else "")}',
            callback_data=callback_factories.SupportCallbackFactory().new(
                is_open='' if is_open is None else 'yes' if is_open else 'no',
                user_id=user_id, request_id=support_request_id, action=''
            )
        )


class DeleteSupportRequestButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, is_open: bool | None, user_id: int | None, support_request_id: int):
        super().__init__(
            '🗑 Delete Request', callback_data=callback_factories.SupportCallbackFactory().new(
                is_open='' if is_open is None else 'yes' if is_open else 'no',
                user_id=user_id, request_id=support_request_id, action='delete')
        )


class CloseSupportRequestButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, is_open: bool | None, user_id: int | None, support_request_id: int):
        super().__init__(
            '⭕ Close Request', callback_data=callback_factories.SupportCallbackFactory().new(
                is_open='' if is_open is None else 'yes' if is_open else 'no',
                user_id=user_id, request_id=support_request_id, action='close')
        )


class AnswerSupportRequestButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, is_open: bool | None, user_id: int | None, support_request_id: int):
        super().__init__(
            '✏️ Answer', callback_data=callback_factories.SupportCallbackFactory().new(
                is_open='' if is_open is None else 'yes' if is_open else 'no',
                user_id=user_id, request_id=support_request_id, action='answer')
        )

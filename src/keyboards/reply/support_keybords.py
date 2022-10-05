import aiogram.types
from keyboards.buttons import support_buttons, navigation_buttons, common_buttons
from services.db_api import schemas


class AdminSupportKeyboard(aiogram.types.ReplyKeyboardMarkup):
    def __init__(self):
        super().__init__(row_width=3, resize_keyboard=True)
        self.add(
            support_buttons.ActiveSupportRequestsButton(),
            support_buttons.ClosedSupportRequestsButton(),
            support_buttons.NewSupportSubjectButton()
        )
        self.row(navigation_buttons.BackButton())


class UserSupportKeyboard(aiogram.types.ReplyKeyboardMarkup):
    def __init__(self):
        super().__init__(row_width=3, resize_keyboard=True)
        self.add(
            support_buttons.NewSupportRequestButton(),
            support_buttons.UsersSupportsButton(),
            support_buttons.NewSupportSubjectButton()
        )
        self.row(navigation_buttons.BackButton())


class NewSupportRequestSubjectsKeyboard(aiogram.types.InlineKeyboardMarkup):
    def __init__(self, subjects: list[schemas.SupportSubject]):
        super().__init__(row_width=1)
        for subject in subjects:
            self.add(support_buttons.NewSupportRequestSubjectButton(subject.id, subject.name))
        self.add(common_buttons.CloseButton())


class SupportRequestsKeyboard(aiogram.types.InlineKeyboardMarkup):
    def __init__(self, support_requests: list[schemas.SupportRequest], is_open: bool = None, user_id: bool = None):
        super().__init__(row_width=1)
        for request in support_requests:
            self.add(support_buttons.SupportRequestButton(is_open, user_id or '', request.id, request.issue))
        self.row(common_buttons.CloseButton())


class SupportRequestMenuKeyboard(aiogram.types.InlineKeyboardMarkup):
    def __init__(self, request_id: int, is_open: bool = None, user_id: int = None):
        super().__init__()
        if user_id is None:
            if is_open:
                self.row(
                    support_buttons.AnswerSupportRequestButton(is_open, user_id or '', request_id),
                    support_buttons.CloseSupportRequestButton(is_open, user_id or '', request_id)
                )
            self.row(support_buttons.DeleteSupportRequestButton(is_open, user_id or '', request_id))
        self.row(common_buttons.CloseButton())

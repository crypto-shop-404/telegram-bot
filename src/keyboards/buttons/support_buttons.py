import aiogram.types


class ActiveSupportRequestsButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='📗 Active Requests')


class ClosedSupportRequestsButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='📕 Closed Requests')


class NewSupportSubjectButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='🆘 New Support Subject')

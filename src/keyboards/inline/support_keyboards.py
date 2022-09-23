import aiogram.types

from keyboards.buttons import support_buttons


class SupportKeyboard(aiogram.types.InlineKeyboardMarkup):
    def __init__(self):
        super().__init__(row_width=3)
        self.add(support_buttons.ActiveSupportRequestsButton())
        self.add(support_buttons.ClosedSupportRequestsButton())
        self.add(support_buttons.NewSupportSubjectButton())

import aiogram.types

from keyboards.buttons import balance_buttons, common_buttons


class TopUpBalanceKeyboard(aiogram.types.InlineKeyboardMarkup):
    def __init__(self):
        super().__init__(row_width=1)
        self.add(balance_buttons.TopUpBalanceButton())
        self.add(common_buttons.CloseButton())

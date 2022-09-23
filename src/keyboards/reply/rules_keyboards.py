import aiogram.types

from keyboards.buttons import rules_buttons


class AcceptRulesKeyboard(aiogram.types.ReplyKeyboardMarkup):
    def __init__(self):
        super().__init__(resize_keyboard=True)
        self.add(rules_buttons.AcceptRulesButton())

import aiogram

from keyboards.buttons import product_management_buttons


class CompleteProductAddingKeyboard(aiogram.types.ReplyKeyboardMarkup):
    def __init__(self):
        super().__init__(resize_keyboard=True)
        self.add(product_management_buttons.CompleteProductAddingKeyboard())

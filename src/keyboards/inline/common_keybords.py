import aiogram.types
import aiogram.utils.callback_data

from keyboards.buttons import common_buttons


class ConfirmationKeyboard(aiogram.types.InlineKeyboardMarkup):
    def __init__(self, callback_factory: aiogram.utils.callback_data.CallbackData, **callback_data):
        super().__init__(row_width=2)
        self.add(
            common_buttons.ConfirmButton(callback_factory, **callback_data),
            common_buttons.CancelButton(callback_factory, **callback_data)
        )


class MockKeyboard(aiogram.types.InlineKeyboardMarkup):
    def __init__(self):
        super().__init__()
        self.add(aiogram.types.InlineKeyboardButton(text='ㅤ', callback_data='-'))

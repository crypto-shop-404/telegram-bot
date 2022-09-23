import aiogram.utils.callback_data


class CloseButton(aiogram.types.InlineKeyboardButton):
    def __init__(self):
        super().__init__(text='🚫 Close', callback_data='close')


class CancelButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, callback_factory: aiogram.utils.callback_data.CallbackData, **callback_data):
        callback_data.pop('@')
        callback_data['is_confirmed'] = 'no'
        super().__init__(
            text='🚫 Cancel',
            callback_data=callback_factory.new(
                **callback_data
            )
        )


class ConfirmButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, callback_factory: aiogram.utils.callback_data.CallbackData, **callback_data):
        callback_data.pop('@')
        callback_data['is_confirmed'] = 'yes'
        super().__init__(
            text='✅ Ok',
            callback_data=callback_factory.new(
                **callback_data
            )
        )

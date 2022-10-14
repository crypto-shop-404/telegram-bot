import aiogram.types
from keyboards.inline import callback_factories


class TopUpBalanceButton(aiogram.types.InlineKeyboardButton):
    def __init__(self):
        super().__init__(
            '🔝 Top Up',
            callback_data=callback_factories.TopUpBalanceCallbackFactory().new(
                amount='', payment_method=''
            )
        )

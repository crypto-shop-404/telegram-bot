import aiogram.types

from keyboards.buttons import payments_management_buttons, common_buttons


class CoinbaseKeyboard(aiogram.types.InlineKeyboardMarkup):
    def __init__(self):
        super().__init__(row_width=1)
        self.add(
            payments_management_buttons.ChangeCoinbaseAPIKey(),
            payments_management_buttons.CheckPaymentSystem('coinbase'),
            common_buttons.CloseButton()
        )

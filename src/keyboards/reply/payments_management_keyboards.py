import aiogram.types

from keyboards.buttons import payments_buttons, navigation_buttons
from repositories import payments_apis_repository


class PaymentsKeyboard(aiogram.types.ReplyKeyboardMarkup):
    def __init__(self):
        super().__init__(row_width=3, resize_keyboard=True)
        buttons = {
            'qiwi': payments_buttons.ManageQIWIButton(),
            'yoomoney': payments_buttons.ManageYooMoneyButton(),
            'minerlock': payments_buttons.ManageMinerlockButton(),
            'coinpayments': payments_buttons.ManageCoinPaymentsButton(),
            'coinbase': payments_buttons.ManageCoinbaseButton(),
        }
        apis_repository = payments_apis_repository.PaymentsAPIsRepository()
        for name, api in apis_repository.get_enabled_apis():
            self.add(buttons[name])
        self.row(navigation_buttons.BackButton())

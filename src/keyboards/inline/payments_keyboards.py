import aiogram.utils.callback_data

from keyboards.buttons import payments_buttons, navigation_buttons
from repositories import payments_apis_repository


class PaymentMethodsKeyboard(aiogram.types.InlineKeyboardMarkup):
    def __init__(self, callback_data: dict[str: str], callback_factory: aiogram.utils.callback_data.CallbackData,
                 is_balance: bool = False, crypto_payments: str = None):
        super().__init__(row_width=1)
        buttons = {
            'qiwi': payments_buttons.QiwiButton(callback_data, callback_factory),
            'yoomoney': payments_buttons.YooMoneyButton(callback_data, callback_factory),
            'minerlock': payments_buttons.MinerlockButton(callback_data, callback_factory),
            'coinpayments': payments_buttons.CoinPaymentsButton(callback_data, callback_factory),
            'coinbase': payments_buttons.CoinBaseButton(callback_data, callback_factory),
            'crypto_payments': payments_buttons.CryptoPaymentButton(callback_data, crypto_payments, callback_factory)
        }
        apis_repository = payments_apis_repository.PaymentsAPIsRepository(crypto_payments)
        for name, api in apis_repository.get_valid_apis():
            self.add(buttons[name])
        if is_balance:
            self.add(payments_buttons.BalanceButton(callback_data, callback_factory))
        self.add(navigation_buttons.InlineBackButton(
            callback_factory.new(**(callback_data | {'quantity': '', 'payment_method': ''})))
        )


class CoinbasePaymentKeyboard(aiogram.types.InlineKeyboardMarkup):
    def __init__(self, payment_url: str):
        super().__init__()
        self.add(payments_buttons.PayWithCoinbaseButton(payment_url))

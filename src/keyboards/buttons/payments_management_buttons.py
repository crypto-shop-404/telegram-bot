import aiogram.types

from keyboards.inline import callback_factories


class QiwiManagementButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='🥝 QIWI')


class YooMoneyManagementButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='💵 YooMoney')


class MinerlockManagementButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='📩 Minerlock')


class CoinpaymentsManagementButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='🔗 Coinpayments')


class CoinbaseManagementButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='🌐 Coinbase')


class CheckPaymentSystem(aiogram.types.InlineKeyboardMarkup):
    def __init__(self, payment_system: str):
        super().__init__(
            text='✅ Check', callback_data=callback_factories.PaymentSystemCallbackFactory().new(
                system=payment_system, action='check'
            )
        )


class ChangeCoinbaseAPIKey(aiogram.types.InlineKeyboardMarkup):
    def __init__(self):
        super().__init__(
            text='🔑 Chane API Key',
            callback_data=callback_factories.PaymentSystemCallbackFactory().new(
                system='coinbase', action='change_api_key'
            )
        )

import aiogram.types


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

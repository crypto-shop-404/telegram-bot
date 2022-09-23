import aiogram.types


class ShopButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='🛒 Products')


class ShopManagementButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='📦 All Products')


class PaymentManagementButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='💳 Payment Management')


class ShopInformationButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='🏪 Shop Information')


class BalanceButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='💲 Balance')


class SupportButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='👨‍💻 Support')


class StatisticsButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='📊 Statistics')


class UserManagementButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='🙍‍♂ Users')


class MailingButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='📧 Newsletter')


class FAQButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='ℹ️ FAQ')


class RulesButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='📗 Rules')


class ProfileButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='📱 Profile')


class BackupButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='💾 Backup')

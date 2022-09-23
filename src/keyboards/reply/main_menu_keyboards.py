import aiogram.types

from keyboards.buttons import main_menu_buttons


class AdminMainMenuKeyboard(aiogram.types.ReplyKeyboardMarkup):
    def __init__(self):
        super().__init__()
        self.row(main_menu_buttons.ShopButton(), main_menu_buttons.ShopManagementButton(),
                 main_menu_buttons.PaymentManagementButton())
        self.row(main_menu_buttons.ShopInformationButton(), main_menu_buttons.BalanceButton())
        self.row(main_menu_buttons.StatisticsButton(), main_menu_buttons.UserManagementButton(),
                 main_menu_buttons.MailingButton())
        self.row(main_menu_buttons.SupportButton(), main_menu_buttons.BackupButton())


class UserMainMenuKeyboard(aiogram.types.ReplyKeyboardMarkup):
    def __init__(self):
        super().__init__()
        self.row(main_menu_buttons.ShopButton())
        self.row(main_menu_buttons.FAQButton(), main_menu_buttons.RulesButton(), main_menu_buttons.BalanceButton())
        self.row(main_menu_buttons.ProfileButton(), main_menu_buttons.SupportButton())

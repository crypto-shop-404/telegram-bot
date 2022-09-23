import aiogram.types

from keyboards.buttons import shop_information_buttons, navigation_buttons


class ShopInformationKeyboard(aiogram.types.ReplyKeyboardMarkup):
    def __init__(self):
        super().__init__()
        self.row(shop_information_buttons.FAQButton, shop_information_buttons.RulesButton)
        self.row(shop_information_buttons.GreetingsButton, shop_information_buttons.ComebackMessageButton)
        self.row(navigation_buttons.BackButton())

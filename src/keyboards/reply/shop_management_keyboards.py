import aiogram.types

from keyboards.buttons import product_management_buttons, category_management_buttons, navigation_buttons


class ShopManagementKeyboard(aiogram.types.ReplyKeyboardMarkup):
    def __init__(self):
        super().__init__(resize_keyboard=True)
        self.row(
            product_management_buttons.ProductManagementButton(),
            category_management_buttons.CategoryManagementButton()
        )
        self.row(navigation_buttons.BackButton())

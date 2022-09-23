import aiogram.types

from keyboards.buttons import product_buttons, common_buttons, navigation_buttons
from keyboards.inline import callback_factories
from services.db_api import schemas


class CategoriesKeyboard(aiogram.types.InlineKeyboardMarkup):
    def __init__(self, categories: list[schemas.Category]):
        super().__init__(row_width=1)
        for category in categories:
            self.add(product_buttons.CategoryButton(category.id, category.name))
        self.add(common_buttons.CloseButton())


class CategoryItemsKeyboard(aiogram.types.InlineKeyboardMarkup):
    def __init__(self, subcategories: list[tuple[int, str, str]], category_id: int):
        super().__init__(row_width=1)
        for item_id, item_name, item_type in subcategories:
            if item_type == 'subcategory':
                self.add(product_buttons.SubcategoryButton(item_id, item_name, category_id))
            elif item_type == 'product':
                self.add(product_buttons.ProductButton(item_id, item_name, category_id))
        self.add(navigation_buttons.InlineBackButton(
            callback_query=callback_factories.ProductCallbackFactory().new(
                action='buy', category_id='', subcategory_id='', product_id=''
            ))
        )
        self.add(common_buttons.CloseButton())


class SubcategoryProductsKeyboard(aiogram.types.InlineKeyboardMarkup):
    def __init__(self, products: list[schemas.Product], category_id: int, subcategory_id: int):
        super().__init__(row_width=1)
        for product in products:
            product_name = f'{product.name} | $ {product.price} | {product.quantity} pc(s)'
            self.add(product_buttons.ProductButton(product.id, product_name, category_id, subcategory_id))
        self.add(navigation_buttons.InlineBackButton(
            callback_query=callback_factories.ProductCallbackFactory().new(
                action='buy', category_id=category_id, subcategory_id='', product_id=''
            ))
        )
        self.add(common_buttons.CloseButton())


class ProductKeyboard(aiogram.types.InlineKeyboardMarkup):
    def __init__(self, product_id: int, available_quantity: int, category_id: int,
                 subcategory_id: int = None, is_available=True):
        super().__init__(row_width=1)
        if is_available:
            self.add(product_buttons.BuyProductButton(product_id, available_quantity))
        self.row(
            navigation_buttons.InlineBackButton(
                callback_factories.ProductCallbackFactory().new(
                    action='buy', category_id=category_id, subcategory_id=subcategory_id or '', product_id='')
            ),
            product_buttons.BackToCategoriesButton()
        )
        self.add(common_buttons.CloseButton())


class ProductQuantityKeyboard(aiogram.types.InlineKeyboardMarkup):
    def __init__(self, product_id: int, available_quantity: int):
        super().__init__(row_width=5)
        self.add(
            *[product_buttons.ProductQuantityButton(product_id, i) for i in range(1, available_quantity + 1)]
        )
        self.row(product_buttons.OwnQuantityButton(product_id, available_quantity))


class PaymentMethodsKeyboard(aiogram.types.InlineKeyboardMarkup):
    def __init__(self, payment_settings: dict):
        super().__init__(row_width=1)

import aiogram.types

from keyboards.inline import callback_factories


class CategoryButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, category_id: int, category_name: str):
        super().__init__(
            text=category_name, callback_data=callback_factories.ProductCallbackFactory().new(
                category_id=category_id, subcategory_id='', product_id='', action='buy'
            )
        )


class SubcategoryButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, subcategory_id: int, subcategory_name: str, category_id: int):
        super().__init__(
            text=subcategory_name, callback_data=callback_factories.ProductCallbackFactory().new(
                category_id=category_id, subcategory_id=subcategory_id, product_id='', action='buy'
            )
        )


class ProductButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, product_id: int, product_name: str, category_id: int, subcategory_id: int = None):
        super().__init__(
            text=product_name, callback_data=callback_factories.ProductCallbackFactory().new(
                category_id=category_id, subcategory_id=subcategory_id or '',
                product_id=product_id, action='buy'
            )
        )


class BuyProductButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, product_id: int, available_quantity: int):
        super().__init__('🛍 Buy', callback_data=callback_factories.BuyProductCallbackFactory().new(
            product_id=product_id, available_quantity=available_quantity, quantity='', payment_method=''
        ))


class ProductQuantityButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, product_id: int, quantity: int):
        super().__init__(
            f'{quantity} pc(s)', callback_data=callback_factories.BuyProductCallbackFactory().new(
                product_id=product_id, available_quantity='',
                quantity=quantity, payment_method=''
            )
        )


class OwnQuantityButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, product_id: int, available_quantity: int):
        super().__init__(
            '🛒 Its value', callback_data=callback_factories.BuyProductCallbackFactory().new(
                product_id=product_id, available_quantity=available_quantity,
                quantity='own', payment_method=''
            )
        )


class BackToCategoriesButton(aiogram.types.InlineKeyboardButton):
    def __init__(self):
        super().__init__('⬅️ Back to categories', callback_data=callback_factories.ProductCallbackFactory().new(
            action='buy', category_id='', subcategory_id='', product_id=''
        ))

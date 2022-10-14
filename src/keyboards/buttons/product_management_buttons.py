import aiogram.types

from keyboards.inline import callback_factories


class ProductManagementButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='📝 Products Management')


class CategoryManagementButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='📁 Categories Control')


class CategoryButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, category_name: str, category_id: int):
        super().__init__(
            text=category_name, callback_data=callback_factories.ProductCallbackFactory().new(
                category_id=category_id, subcategory_id='', product_id='', action='manage'
            )
        )


class SubcategoryButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, category_id: int, subcategory_id: int, subcategory_name: str):
        super().__init__(
            text=subcategory_name, callback_data=callback_factories.ProductCallbackFactory().new(
                category_id=category_id, subcategory_id=subcategory_id, product_id='', action='manage'
            )
        )


class AddProductButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, category_id: int = None, subcategory_id: int = None):
        super().__init__('📓 Add Products', callback_data=callback_factories.ProductCallbackFactory().new(
            category_id=category_id or '', subcategory_id=subcategory_id or '',
            product_id='', action='add'
        ))


class CompleteProductAddingKeyboard(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__('✅ Complete')


class ProductButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, category_id: int, product_id: int,
                 product_text: str):
        super().__init__(
            text=product_text,
            callback_data=callback_factories.ProductCallbackFactory().new(
                category_id=category_id, subcategory_id='', product_id=product_id, action='manage'
            )
        )


class EditProductTitleButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, product_id: int, category_id: int, subcategory_id: int = None):
        super().__init__(
            text='📙 Change Title', callback_data=callback_factories.ProductCallbackFactory().new(
                category_id=category_id, subcategory_id=subcategory_id or '',
                product_id=product_id, action='edit_title'
            )
        )


class EditProductDescriptionButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, product_id: int, category_id: int, subcategory_id: int = None):
        super().__init__(
            text='📋 Edit Description', callback_data=callback_factories.ProductCallbackFactory().new(
                category_id=category_id, subcategory_id=subcategory_id or '',
                product_id=product_id, action='edit_description'
            )
        )


class EditProductPictureButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, product_id: int, category_id: int, subcategory_id: int = None):
        super().__init__(
            text='📋 Change the Image', callback_data=callback_factories.ProductCallbackFactory().new(
                category_id=category_id, subcategory_id=subcategory_id or '',
                product_id=product_id, action='edit_picture'
            )
        )


class EditProductPrice(aiogram.types.InlineKeyboardButton):
    def __init__(self, product_id: int, category_id: int, subcategory_id: int = None):
        super().__init__(
            text='💵 Change the price', callback_data=callback_factories.ProductCallbackFactory().new(
                category_id=category_id, subcategory_id=subcategory_id or '',
                product_id=product_id, action='edit_price'
            )
        )


class ProductUnitsManagementButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, product_id: int, category_id: int, subcategory_id: int = None):
        super().__init__(
            text='📦 Manage Data', callback_data=callback_factories.ProductCallbackFactory().new(
                category_id=category_id, subcategory_id=subcategory_id or '',
                product_id=product_id, action='units'
            )
        )


class AddProductUnitsButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, product_id: int, category_id: int, subcategory_id: int = None):
        super().__init__(
            text='📓 Data transfer', callback_data=callback_factories.ProductCallbackFactory().new(
                category_id=category_id, subcategory_id=subcategory_id or '',
                product_id=product_id, action='add_units'
            )
        )


class DeleteAllProductUnits(aiogram.types.InlineKeyboardButton):
    def __init__(self, product_id: int, category_id: int, subcategory_id: int = None):
        super().__init__(
            text='🗑 Remove Data', callback_data=callback_factories.ProductCallbackFactory().new(
                category_id=category_id, subcategory_id=subcategory_id or '',
                product_id=product_id, action='delete_units'
            )
        )


class DeleteProductButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, product_id: int, category_id: int, subcategory_id: int = None):
        super().__init__(
            text='🗑 Remove Product', callback_data=callback_factories.ProductCallbackFactory().new(
                category_id=category_id, subcategory_id=subcategory_id or '',
                product_id=product_id, action='delete'
            )
        )


class ProductUnitButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, content: str, category_id: int, product_id: int,
                 product_unit_id: int, subcategory_id: int = None):
        super().__init__(
            text=content, callback_data=callback_factories.ProductUnitCallbackFactory().new(
                category_id=category_id, subcategory_id=subcategory_id or '',
                product_id=product_id, id=product_unit_id, action='manage',
            )
        )


class EditProductUnitButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, product_unit_id: int, category_id: int, subcategory_id: int, product_id: int):
        super().__init__(
            text='📝 Edit', callback_data=callback_factories.ProductUnitCallbackFactory().new(
                id=product_unit_id, category_id=category_id,
                subcategory_id=subcategory_id or '', product_id=product_id, action='edit'
            )
        )


class DeleteProductUnitButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, product_unit_id: int, category_id: int, subcategory_id: int, product_id: int):
        super().__init__(
            text='🗑 Delete', callback_data=callback_factories.ProductUnitCallbackFactory().new(
                id=product_unit_id, category_id=category_id,
                subcategory_id=subcategory_id or '', product_id=product_id, action='delete'
            )
        )


class BackToCategoriesButtons(aiogram.types.InlineKeyboardButton):
    def __init__(self):
        super().__init__(
            '⬅️ Back to category',
            callback_data=callback_factories.ProductCallbackFactory().new(
                category_id='', subcategory_id='', product_id='', action='manage'
            )
        )

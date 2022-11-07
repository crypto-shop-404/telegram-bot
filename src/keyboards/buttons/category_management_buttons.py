import aiogram.types

from keyboards.inline import callback_factories


class CategoryManagementButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='📁 Categories Control')


class CategoryButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, category_name: str, category_id: int):
        super().__init__(
            text=category_name, callback_data=callback_factories.CategoryCallbackFactory().new(
                action='manage', category_id=category_id, subcategory_id=''
            )
        )


class AddCategoriesButton(aiogram.types.InlineKeyboardButton):
    def __init__(self):
        super().__init__(
            '📂 Add category', callback_data=callback_factories.CategoriesCallbackFactory().new(
                action='add'
            )
        )


class AddSubcategoriesButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, category_id: int):
        super().__init__(
            text='📂 Add subcategory', callback_data=callback_factories.CategoryCallbackFactory().new(
                action='add_subcategory', category_id=category_id, subcategory_id=''
            )
        )


class DeleteSubcategoriesButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, category_id: int):
        super().__init__(
            text='🗑 Remove subcategories', callback_data=callback_factories.CategoryCallbackFactory().new(
                action='delete_subcategories', category_id=category_id, subcategory_id=''
            )
        )


class DeleteCategoryButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, category_id: int):
        super().__init__(
            text='🗑 Delete Category', callback_data=callback_factories.CategoryCallbackFactory().new(
                action='delete', category_id=category_id, subcategory_id=''
            )
        )


class SubcategoryForRemovalButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, subcategory_name: str, subcategory_id: int, category_id: int):
        super().__init__(
            text=subcategory_name, callback_data=callback_factories.CategoryCallbackFactory().new(
                action='delete', subcategory_id=subcategory_id, category_id=category_id
            )
        )

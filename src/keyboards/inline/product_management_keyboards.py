import aiogram.types

from keyboards.buttons import product_management_buttons, navigation_buttons, common_buttons
from keyboards.inline import callback_factories
from services.db_api import schemas


class CategoriesKeyboard(aiogram.types.InlineKeyboardMarkup):
    def __init__(self, categories: list[schemas.Category]):
        super().__init__(row_width=1)
        for category in categories:
            self.add(product_management_buttons.CategoryButton(category.name, category.id))
        self.add(common_buttons.CloseButton())


class CategoryItemsKeyboard(aiogram.types.InlineKeyboardMarkup):
    def __init__(self, items: list[tuple[int, str, str]], category_id: int):
        super().__init__(row_width=1)
        for item_id, item_name, item_type in items:
            if item_type == 'subcategory':
                self.add(product_management_buttons.SubcategoryButton(category_id, item_id, item_name))
            elif item_type == 'product':
                self.add(product_management_buttons.ProductButton(category_id, item_id, item_name))
        self.add(product_management_buttons.AddProductButton(category_id))
        self.add(navigation_buttons.InlineBackButton(
            callback_query=callback_factories.ProductCallbackFactory().new(
                category_id='', subcategory_id='', product_id='', action='manage'
            )
        ))
        self.add(common_buttons.CloseButton())


class SubcategoryProductsKeyboard(aiogram.types.InlineKeyboardMarkup):
    def __init__(self, products: list[schemas.Product], subcategory_id: int, category_id: int):
        super().__init__(row_width=1)
        for product in products:
            self.add(product_management_buttons.ProductButton(
                category_id, product.id, f'{product.name} | ${product.price} | {product.quantity} pc(s)')
            )
        self.add(product_management_buttons.AddProductButton(category_id, subcategory_id=subcategory_id))
        self.add(navigation_buttons.InlineBackButton(
            callback_query=callback_factories.ProductCallbackFactory().new(
                category_id=category_id, subcategory_id='', product_id='', action='manage'))
        )
        self.add(common_buttons.CloseButton())


class ProductKeyboard(aiogram.types.InlineKeyboardMarkup):
    def __init__(self, category_id: int, product_id: int, subcategory_id: int = None):
        super().__init__(row_width=1)
        self.add(
            product_management_buttons.EditProductTitleButton(product_id, category_id, subcategory_id),
            product_management_buttons.EditProductDescriptionButton(product_id, category_id, subcategory_id),
            product_management_buttons.EditProductPictureButton(product_id, category_id, subcategory_id),
            product_management_buttons.EditProductPrice(product_id, category_id, subcategory_id),
            product_management_buttons.ProductUnitsManagementButton(product_id, category_id, subcategory_id)
        )
        self.row(
            product_management_buttons.AddProductUnitsButton(product_id, category_id, subcategory_id),
            product_management_buttons.DeleteAllProductUnits(product_id, category_id, subcategory_id))
        self.add(product_management_buttons.DeleteProductButton(product_id, category_id, subcategory_id))
        self.row(
            navigation_buttons.InlineBackButton(
                callback_query=callback_factories.ProductCallbackFactory().new(
                    category_id=category_id, subcategory_id=subcategory_id or '',
                    product_id='', action='manage'
                )
            ), product_management_buttons.BackToCategoriesButtons())
        self.add(common_buttons.CloseButton())


class ProductUnitsKeyboard(aiogram.types.InlineKeyboardMarkup):
    def __init__(self, category_id: int, product_id: int,
                 product_units: list[schemas.ProductUnit],
                 subcategory_id: int = None):
        super().__init__()
        for unit in product_units:
            self.row(product_management_buttons.ProductUnitButton(
                unit.content, category_id, product_id, unit.id, subcategory_id
            ))
        self.row(navigation_buttons.InlineBackButton(
            callback_query=callback_factories.ProductCallbackFactory().new(
                category_id=category_id, subcategory_id=subcategory_id or '',
                product_id=product_id, action='manage'
            )
        ))
        self.row(common_buttons.CloseButton())


class ProductUnitKeyboard(aiogram.types.InlineKeyboardMarkup):
    def __init__(self, category_id: int, product_id: int, product_unit_id: int, subcategory_id: int = None):
        super().__init__()
        self.row(
            product_management_buttons.EditProductUnitButton(
                product_unit_id, category_id, subcategory_id, product_id
            ),
            product_management_buttons.DeleteProductUnitButton(
                product_unit_id, category_id, subcategory_id, product_id
            )
        )
        self.row(navigation_buttons.InlineBackButton(
            callback_query=callback_factories.ProductCallbackFactory().new(
                action='manage', category_id=category_id,
                subcategory_id=subcategory_id or '', product_id=product_id
            )
        ))

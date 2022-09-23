import aiogram.types

import config
import responses.product_management
from keyboards.inline import callback_factories
from loader import dp
from services import db_api
from services.db_api import queries
from utils import file_system


@dp.callback_query_handler(callback_factories.ProductCallbackFactory().filter(
    action='delete'
))
async def delete_product(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    category_id = int(callback_data['category_id'])
    subcategory_id = callback_data['subcategory_id']
    product_id = int(callback_data['product_id'])
    with db_api.create_session() as session:
        product = queries.get_product(session, product_id)
        if product.picture is not None:
            file_system.delete_file(config.PRODUCT_PICTURE_PATH / product.picture)
        for product_unit in queries.get_not_sold_product_units(session, product_id):
            file_system.delete_file(config.PRODUCT_UNITS_PATH / product_unit.content)
        queries.delete_product(session, product_id)
        session.flush()
        await responses.product_management.SuccessRemovalUnitResponse(query)
        if subcategory_id != '':
            subcategory_id = int(subcategory_id)
            products = queries.get_category_products(session, subcategory_id=subcategory_id)
            await responses.product_management.SubcategoryProductsResponse(
                query, category_id, subcategory_id, products
            )
        else:
            items = queries.get_category_items(session, category_id)
            await responses.product_management.CategoryItemsResponse(query, items, category_id)

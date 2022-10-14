import aiogram.types

import responses.product_management
from filters import is_admin, is_user_in_db
from keyboards.inline import callback_factories
from loader import dp
from services import db_api, product_services
from services.db_api import queries


@dp.callback_query_handler(callback_factories.ProductCallbackFactory().filter(action='delete'),
                           is_admin.IsUserAdmin(), is_user_in_db.IsUserInDB())
async def delete_product(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    category_id = int(callback_data['category_id'])
    subcategory_id = callback_data['subcategory_id']
    product_id = int(callback_data['product_id'])
    with db_api.create_session() as session:
        product_services.ProductLifeCycle(product_id=product_id).load_from_db(session).delete(session)
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


@dp.callback_query_handler(callback_factories.ProductCallbackFactory().filter(action='delete_units'),
                           is_admin.IsUserAdmin(), is_user_in_db.IsUserInDB())
async def delete_product_units(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    category_id, subcategory_id = callback_data['category_id'], callback_data['subcategory_id']
    category_id = int(category_id) if category_id != '' else None
    subcategory_id = int(subcategory_id) if subcategory_id != '' else None
    product_id = int(callback_data['product_id'])
    with db_api.create_session() as session:
        product_life_cycle = product_services.ProductLifeCycle(
            product_id=product_id).load_from_db(session).delete_product_units(session)
        product = queries.get_product(session, product_id)
        await responses.product_management.ProductResponse(
            query, product, category_id, subcategory_id
        )

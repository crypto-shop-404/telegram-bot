import aiogram
from aiogram import filters

import responses.main_menu
import responses.product_management
from keyboards.inline import callback_factories
from loader import dp
from services import db_api
from services.db_api import queries


@dp.message_handler(filters.Text('📝 Products Management'))
async def product_categories(message: aiogram.types.Message):
    with db_api.create_session() as session:
        categories = queries.get_all_categories(session)
        await responses.product_management.ProductCategoriesResponse(message, categories)


@dp.callback_query_handler(callback_factories.ProductCallbackFactory().filter(
    category_id='', subcategory_id='', product_id='', action='manage')
)
async def product_categories(query: aiogram.types.CallbackQuery):
    with db_api.create_session() as session:
        categories = queries.get_all_categories(session)
        await responses.product_management.ProductCategoriesResponse(query, categories)


@dp.callback_query_handler(
    callback_factories.ProductCallbackFactory().filter(subcategory_id='', product_id='', action='manage'))
async def category_items(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    category_id = int(callback_data['category_id'])
    with db_api.create_session() as session:
        items = queries.get_category_items(session, category_id=category_id)
    await responses.product_management.CategoryItemsResponse(query, items, category_id)


@dp.callback_query_handler(
    callback_factories.ProductCallbackFactory().filter(
        product_id='', action='manage')
)
async def subcategory_products(query: aiogram.types, callback_data: dict[str, str]):
    subcategory_id = int(callback_data['subcategory_id'])
    with db_api.create_session() as session:
        products = queries.get_category_products(session, subcategory_id=subcategory_id)
        await responses.product_management.SubcategoryProductsResponse(
            query, int(callback_data['category_id']), subcategory_id, products
        )


@dp.callback_query_handler(callback_factories.ProductCallbackFactory().filter(
    action='manage',
))
async def product_menu(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    category_id, subcategory_id = callback_data['category_id'], callback_data['subcategory_id']
    category_id = int(category_id) if category_id != '' else None
    subcategory_id = int(subcategory_id) if subcategory_id != '' else None
    with db_api.create_session() as session:
        product = queries.get_product(session, int(callback_data['product_id']))
        await responses.product_management.ProductResponse(
            query, product, category_id, subcategory_id
        )

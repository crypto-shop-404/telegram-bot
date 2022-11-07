import aiogram
from aiogram import filters

import responses.category_management
import responses.main_menu
from filters import is_admin
from keyboards.inline import callback_factories
from loader import dp
from services import db_api
from services.db_api import queries


@dp.message_handler(filters.Text('📁 Categories Control'), is_admin.IsUserAdmin())
async def categories(message: aiogram.types.Message):
    with db_api.create_session() as session:
        await responses.category_management.CategoriesResponse(
            message, queries.get_all_categories(session)
        )


@dp.callback_query_handler(
    callback_factories.CategoriesCallbackFactory().filter(action='manage'), is_admin.IsUserAdmin())
async def categories(query: aiogram.types.CallbackQuery):
    with db_api.create_session() as session:
        await responses.category_management.CategoriesResponse(
            query, queries.get_all_categories(session)
        )


@dp.callback_query_handler(callback_factories.CategoryCallbackFactory().filter(
    action='manage', subcategory_id=''), is_admin.IsUserAdmin()
)
async def category_menu(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    category_id = int(callback_data['category_id'])
    with db_api.create_session() as session:
        category_name = queries.get_category(session, category_id).name
        subcategory_list = queries.get_subcategories(session, category_id)
        await responses.category_management.CategoryMenuResponse(
            query, category_id, category_name, subcategory_list
        )

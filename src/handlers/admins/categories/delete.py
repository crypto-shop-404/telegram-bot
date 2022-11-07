import aiogram
from aiogram.dispatcher import handler

import responses.category_management
import responses.main_menu
from filters import is_admin
from keyboards.inline import callback_factories
from loader import dp
from services import db_api
from services.db_api import queries


@dp.callback_query_handler(callback_factories.CategoryCallbackFactory().filter(
    action='delete', subcategory_id='', is_confirmed=''), is_admin.IsUserAdmin()
)
async def delete_category(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    category_id = int(callback_data['category_id'])
    with db_api.create_session() as session:
        await responses.category_management.ConfirmationRemovalCategoryResponse(
            query, queries.count_subcategories(session, category_id),
            queries.count_products(session, category_id), callback_data
        )


@dp.callback_query_handler(callback_factories.CategoryCallbackFactory().filter(
    action='delete', subcategory_id=''), is_admin.IsUserAdmin()
)
async def delete_category(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    with db_api.create_session() as session:
        if callback_data['is_confirmed'] == 'no':
            category_id = int(callback_data['category_id'])
            category_name = queries.get_category(session, category_id).name
            subcategory_list = queries.get_subcategories(session, category_id)
            await responses.category_management.CategoryMenuResponse(
                query, category_id, category_name, subcategory_list
            )
            raise handler.CancelHandler
        queries.delete_category(session, int(callback_data['category_id']))
        await responses.category_management.SuccessRemovalCategoryResponse(query)
        await responses.category_management.CategoriesResponse(
            query.message, queries.get_all_categories(session)
        )


@dp.callback_query_handler(callback_factories.CategoryCallbackFactory().filter(
    action='delete_subcategories', subcategory_id=''), is_admin.IsUserAdmin()
)
async def subcategories_for_removal(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    category_id = int(callback_data['category_id'])
    with db_api.create_session() as session:
        subcategory_list = queries.get_subcategories(session, category_id)
        await responses.category_management.DeleteSubcategoriesResponse(
            query, subcategory_list, category_id
        )


@dp.callback_query_handler(
    callback_factories.CategoryCallbackFactory().filter(
        action='delete', is_confirmed=''), is_admin.IsUserAdmin()
)
async def delete_subcategory(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    category_id = int(callback_data['category_id'])
    subcategory_id = int(callback_data['subcategory_id'])
    with db_api.create_session() as session:
        await responses.category_management.ConfirmationRemovalSubcategoryResponse(
            query, queries.count_products(session, category_id, subcategory_id), callback_data
        )


@dp.callback_query_handler(callback_factories.CategoryCallbackFactory().filter(
    action='delete'), is_admin.IsUserAdmin()
)
async def delete_subcategory(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    with db_api.create_session() as session:
        category_id = int(callback_data['category_id'])
        subcategory_list = queries.get_subcategories(session, category_id)
        if callback_data['is_confirmed'] == 'no':
            await responses.category_management.DeleteSubcategoriesResponse(
                query, subcategory_list, category_id
            )
            raise handler.CancelHandler
        queries.delete_subcategory(session, int(callback_data['subcategory_id']))
    with db_api.create_session() as session:
        subcategory_list = queries.get_subcategories(session, category_id)
        await responses.category_management.SuccessRemovalCategoryResponse(query)
        await responses.category_management.DeleteSubcategoriesResponse(
            query.message, subcategory_list, category_id
        )

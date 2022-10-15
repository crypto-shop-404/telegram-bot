import aiogram
from aiogram import dispatcher
from aiogram import filters

import responses.category_management
from filters import is_admin
from keyboards.inline import callback_factories
from loader import dp
from services import db_api
from services.db_api import queries
from states import category_states


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


@dp.callback_query_handler(
    callback_factories.CategoriesCallbackFactory().filter(action='add'), is_admin.IsUserAdmin())
async def add_categories(query: aiogram.types.CallbackQuery):
    await responses.category_management.AddCategoriesResponse(query)
    await category_states.AddCategories.waiting_category_name.set()


@dp.message_handler(is_admin.IsUserAdmin(), state=category_states.AddCategories.waiting_category_name)
async def add_categories(message: aiogram.types.Message, state: dispatcher.FSMContext):
    await state.finish()
    category_list = message.text.split('\n')
    with db_api.create_session() as session:
        queries.add_categories(session, category_list)
    await responses.category_management.SuccessAddingCategoryResponse(message, len(category_list))
    with db_api.create_session() as session:
        await responses.category_management.CategoriesResponse(
            message, queries.get_all_categories(session)
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


@dp.callback_query_handler(callback_factories.CategoryCallbackFactory().filter(
    action='delete', subcategory_id=''), is_admin.IsUserAdmin()
)
async def delete_category(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    with db_api.create_session() as session:
        queries.delete_category(session, int(callback_data['category_id']))
    await responses.category_management.SuccessRemovalCategoryResponse(query)
    with db_api.create_session() as session:
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
    callback_factories.CategoryCallbackFactory().filter(action='delete'), is_admin.IsUserAdmin())
async def delete_subcategory(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    category_id = int(callback_data['category_id'])
    with db_api.create_session() as session:
        queries.delete_subcategory(session, int(callback_data['subcategory_id']))
        await responses.category_management.SuccessRemovalSubcategoryResponse(query)
        subcategory_list = queries.get_subcategories(session, category_id)
        await responses.category_management.DeleteSubcategoriesResponse(
            query, subcategory_list, category_id
        )


@dp.callback_query_handler(callback_factories.CategoryCallbackFactory().filter(
    action='add_subcategories', subcategory_id=''), is_admin.IsUserAdmin()
)
async def add_subcategories(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    await category_states.AddSubcategories.waiting_subcategory_name.set()
    await dp.current_state().update_data({'category_id': int(callback_data['category_id'])})
    await responses.category_management.AddCategoriesResponse(query)


@dp.message_handler(is_admin.IsUserAdmin(),
                    state=category_states.AddSubcategories.waiting_subcategory_name)
async def add_subcategories(message: aiogram.types.Message, state: dispatcher.FSMContext):
    state_data = await state.get_data()
    await state.finish()
    category_id = state_data['category_id']
    subcategory_names = message.text.split('\n')
    with db_api.create_session() as session:
        queries.add_subcategories(session, subcategory_names, category_id)
    await responses.category_management.SuccessAddingCategoryResponse(message, len(subcategory_names))
    with db_api.create_session() as session:
        await responses.category_management.CategoryMenuResponse(
            message, category_id, queries.get_category(session, category_id).name,
            queries.get_subcategories(session, category_id)
        )

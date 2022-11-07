import aiogram
from aiogram import dispatcher

import responses.category_management
import responses.main_menu
from filters import is_admin
from keyboards.inline import callback_factories
from loader import dp
from services import db_api
from services.db_api import queries
from states import category_states


@dp.callback_query_handler(
    callback_factories.CategoriesCallbackFactory().filter(action='add'), is_admin.IsUserAdmin())
async def add_category(query: aiogram.types.CallbackQuery):
    await responses.category_management.AddCategoriesResponse(query)
    await category_states.AddCategories.waiting_title.set()


@dp.message_handler(is_admin.IsUserAdmin(), state=category_states.AddCategories.waiting_title)
async def add_category(message: aiogram.types.Message, state: dispatcher.FSMContext):
    await state.finish()
    with db_api.create_session() as session:
        queries.add_category(session, message.text)
    await responses.category_management.SuccessAddingCategoryResponse(message)
    with db_api.create_session() as session:
        await responses.category_management.CategoriesResponse(
            message, queries.get_all_categories(session)
        )


@dp.callback_query_handler(callback_factories.CategoryCallbackFactory().filter(
    action='add_subcategory', subcategory_id=''), is_admin.IsUserAdmin()
)
async def add_subcategory(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    await category_states.AddSubcategories.waiting_title.set()
    await dp.current_state().update_data({'category_id': int(callback_data['category_id'])})
    await responses.category_management.AddCategoriesResponse(query)


@dp.message_handler(is_admin.IsUserAdmin(), state=category_states.AddSubcategories.waiting_title)
async def add_subcategory(message: aiogram.types.Message, state: dispatcher.FSMContext):
    state_data = await state.get_data()
    await state.finish()
    category_id = state_data['category_id']
    with db_api.create_session() as session:
        queries.add_subcategory(session, message.text, category_id)
        await responses.category_management.SuccessAddingCategoryResponse(message)
        await responses.category_management.CategoryMenuResponse(
            message, category_id, queries.get_category(session, category_id).name,
            queries.get_subcategories(session, category_id)
        )

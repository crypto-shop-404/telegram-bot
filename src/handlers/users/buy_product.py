import aiogram.types
from aiogram import filters, dispatcher

import config
import responses.products
from filters import is_user_in_db
from keyboards.inline import callback_factories
from loader import dp
from services import db_api
from services.db_api import queries
from states import product_states


@dp.message_handler(is_user_in_db.IsUserInDB(), filters.Text('🛒 Products'))
async def categories(message: aiogram.types.Message):
    with db_api.create_session() as session:
        category_list = queries.get_all_categories(session)
        await responses.products.CategoriesResponses(message, category_list)


@dp.callback_query_handler(is_user_in_db.IsUserInDB(), callback_factories.ProductCallbackFactory().filter(
    action='buy', category_id='', subcategory_id='', product_id=''
))
async def categories(query: aiogram.types.CallbackQuery):
    with db_api.create_session() as session:
        category_list = queries.get_all_categories(session)
        await responses.products.CategoriesResponses(query, category_list)


@dp.callback_query_handler(is_user_in_db.IsUserInDB(), callback_factories.ProductCallbackFactory().filter(
    action='buy', subcategory_id='', product_id=''
))
async def category_items(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    category_id = int(callback_data['category_id'])
    with db_api.create_session() as session:
        category_item_list = queries.get_category_items(session, category_id)
        await responses.products.CategoryItemsResponse(query, category_item_list, category_id)


@dp.callback_query_handler(
    is_user_in_db.IsUserInDB(), callback_factories.ProductCallbackFactory().filter(action='buy', product_id='')
)
async def subcategory_products(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    category_id = int(callback_data['category_id'])
    subcategory_id = callback_data['subcategory_id']
    subcategory_id = int(subcategory_id) if subcategory_id != '' else None
    with db_api.create_session() as session:
        products = queries.get_category_products(session, category_id, subcategory_id)
        await responses.products.SubcategoryProductsResponse(
            query, category_id, subcategory_id, products
        )


@dp.callback_query_handler(is_user_in_db.IsUserInDB(),
                           callback_factories.ProductCallbackFactory().filter(action='buy'))
async def product_menu(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    product_id = int(callback_data['product_id'])
    subcategory_id = callback_data['subcategory_id']
    category_id = int(callback_data['category_id'])
    subcategory_id = subcategory_id if subcategory_id != '' else None

    with db_api.create_session() as session:
        product = queries.get_product(session, product_id)
        product_picture = open(config.PRODUCT_PICTURE_PATH / product.picture, 'rb')
        await responses.products.ProductResponse(
            query, product, category_id, subcategory_id, product_picture
        )


@dp.callback_query_handler(is_user_in_db.IsUserInDB(),
                           callback_factories.BuyProductCallbackFactory().filter(quantity='', payment_method=''))
async def product_quantity(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    await responses.products.ProductQuantityResponse(
        query, int(callback_data['product_id']), int(callback_data['available_quantity'])
    )


@dp.callback_query_handler(is_user_in_db.IsUserInDB(),
                           callback_factories.BuyProductCallbackFactory().filter(quantity='own', payment_method=''))
async def own_product_quantity(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    await product_states.EnterProductQuantity.waiting_quantity.set()
    await dp.current_state().update_data(callback_data)
    await responses.products.OwnProductQuantityResponse(
        query, int(callback_data['available_quantity'])
    )


@dp.message_handler(is_user_in_db.IsUserInDB(), state=product_states.EnterProductQuantity.waiting_quantity)
async def own_product_quantity(message: aiogram.types.Message, state: dispatcher.FSMContext):
    quantity = message.text
    if isinstance(quantity, str) and quantity.isdigit() and int(quantity) > 0:
        await state.finish()
        await responses.products.PaymentMethodResponse(message)
    else:
        await responses.products.IncorrectQuantity(message)


@dp.callback_query_handler(is_user_in_db.IsUserInDB(),
                           callback_factories.BuyProductCallbackFactory().filter(payment_method=''))
async def payment_method(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    await responses.products.PaymentMethodResponse(query)

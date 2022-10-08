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


@dp.message_handler(filters.Text('🛒 Products'), is_user_in_db.IsUserInDB())
async def categories(message: aiogram.types.Message):
    with db_api.create_session() as session:
        category_list = queries.get_all_categories(session)
        await responses.products.CategoriesResponses(message, category_list)


@dp.callback_query_handler(callback_factories.ProductCallbackFactory().filter(
    action='buy', category_id='', subcategory_id='', product_id=''), is_user_in_db.IsUserInDB()
)
async def categories(query: aiogram.types.CallbackQuery):
    with db_api.create_session() as session:
        category_list = queries.get_all_categories(session)
        await responses.products.CategoriesResponses(query, category_list)


@dp.callback_query_handler(callback_factories.ProductCallbackFactory().filter(
    action='buy', subcategory_id='', product_id=''), is_user_in_db.IsUserInDB()
)
async def category_items(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    category_id = int(callback_data['category_id'])
    with db_api.create_session() as session:
        category_item_list = queries.get_category_items(session, category_id)
        await responses.products.CategoryItemsResponse(query, category_item_list, category_id)


@dp.callback_query_handler(
    callback_factories.ProductCallbackFactory().filter(action='buy', product_id=''), is_user_in_db.IsUserInDB()
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


@dp.callback_query_handler(
    callback_factories.ProductCallbackFactory().filter(action='buy'), is_user_in_db.IsUserInDB()
)
async def product_menu(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    product_id = int(callback_data['product_id'])
    subcategory_id = callback_data['subcategory_id']
    category_id = int(callback_data['category_id'])
    subcategory_id = subcategory_id if subcategory_id != '' else None

    with db_api.create_session() as session:
        product = queries.get_product(session, product_id)
        if product.picture is not None:
            product_picture = open(config.PRODUCT_PICTURE_PATH / product.picture, 'rb')
        else:
            product_picture = None
        await responses.products.ProductResponse(
            query, product, category_id, subcategory_id, product_picture
        )


@dp.callback_query_handler(
    callback_factories.BuyProductCallbackFactory().filter(quantity='', payment_method=''), is_user_in_db.IsUserInDB()
)
async def product_quantity(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    await responses.products.ProductQuantityResponse(
        query, int(callback_data['product_id']), int(callback_data['available_quantity'])
    )


@dp.callback_query_handler(
    callback_factories.BuyProductCallbackFactory().filter(quantity='another', payment_method=''),
    is_user_in_db.IsUserInDB()
)
async def own_product_quantity(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    await product_states.EnterProductQuantity.waiting_quantity.set()
    await dp.current_state().update_data(callback_data)
    await responses.products.OwnProductQuantityResponse(
        query, int(callback_data['available_quantity'])
    )


@dp.callback_query_handler(
    callback_factories.BuyProductCallbackFactory().filter(payment_method=''), is_user_in_db.IsUserInDB()
)
async def product_quantity(query: aiogram.types.CallbackQuery, callback_data: dict[str: str]):
    await responses.products.PaymentMethodResponse(
        query, callback_data, crypto_payments=config.PaymentsSettings().crypto_payments
    )


@dp.message_handler(is_user_in_db.IsUserInDB(), state=product_states.EnterProductQuantity.waiting_quantity)
async def another_product_quantity(message: aiogram.types.Message, state: dispatcher.FSMContext):
    quantity = message.text
    callback_data = (await state.get_data())['callback_data']
    await state.finish()
    if isinstance(quantity, str) and quantity.isdigit() and int(quantity) > 0:
        await responses.products.PaymentMethodResponse(
            message, callback_data, crypto_payments=config.PaymentsSettings().crypto_payments
        )
    else:
        await responses.products.IncorrectQuantity(message)


@dp.callback_query_handler(callback_factories.BuyProductCallbackFactory().filter(payment_method='qiwi'),
                           is_user_in_db.IsUserInDB())
async def qiwi(query: aiogram.types.CallbackQuery):
    await query.message.answer('🚧 Under Development')


@dp.callback_query_handler(callback_factories.BuyProductCallbackFactory().filter(payment_method='yoomoney'),
                           is_user_in_db.IsUserInDB())
async def yoomoney(query: aiogram.types.CallbackQuery):
    await query.message.answer('🚧 Under Development')


@dp.callback_query_handler(callback_factories.BuyProductCallbackFactory().filter(payment_method='minerlock'),
                           is_user_in_db.IsUserInDB())
async def minerlock(query: aiogram.types.CallbackQuery):
    await query.message.answer('🚧 Under Development')


@dp.callback_query_handler(callback_factories.BuyProductCallbackFactory().filter(payment_method='coinpayments'),
                           is_user_in_db.IsUserInDB())
async def coinpayments(query: aiogram.types.CallbackQuery):
    await query.message.answer('🚧 Under Development')


@dp.callback_query_handler(callback_factories.BuyProductCallbackFactory().filter(payment_method='coinbase'),
                           is_user_in_db.IsUserInDB())
async def coinbase(query: aiogram.types.CallbackQuery):
    await query.message.answer('🚧 Under Development')

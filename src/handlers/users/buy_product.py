import decimal

import aiogram.types
from aiogram import filters, dispatcher

import config
import exceptions
import responses.payments
import responses.products
from keyboards.inline import callback_factories
from loader import dp
from services import db_api, notifications
from services.db_api import queries
from services.payments_apis import coinbase_api
from states import product_states


@dp.message_handler(filters.Text('🛒 Products'), filters.ChatTypeFilter(aiogram.types.ChatType.PRIVATE))
async def categories(message: aiogram.types.Message):
    with db_api.create_session() as session:
        if not queries.check_is_user_exists(session, message.from_user.id):
            raise exceptions.UserNotInDatabase
        category_list = queries.get_all_categories(session)
        await responses.products.CategoriesResponses(message, category_list)


@dp.callback_query_handler(callback_factories.ProductCallbackFactory().filter(
    action='buy', category_id='', subcategory_id='', product_id=''),
    filters.ChatTypeFilter(aiogram.types.ChatType.PRIVATE)
)
async def categories(query: aiogram.types.CallbackQuery):
    with db_api.create_session() as session:
        if not queries.check_is_user_exists(session, query.from_user.id):
            raise exceptions.UserNotInDatabase
        category_list = queries.get_all_categories(session)
        await responses.products.CategoriesResponses(query, category_list)


@dp.callback_query_handler(callback_factories.ProductCallbackFactory().filter(
    action='buy', subcategory_id='', product_id=''), filters.ChatTypeFilter(aiogram.types.ChatType.PRIVATE))
async def category_items(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    category_id = int(callback_data['category_id'])
    with db_api.create_session() as session:
        if not queries.check_is_user_exists(session, query.from_user.id):
            raise exceptions.UserNotInDatabase
        category_item_list = queries.get_category_items(session, category_id)
        await responses.products.CategoryItemsResponse(query, category_item_list, category_id)


@dp.callback_query_handler(
    callback_factories.ProductCallbackFactory().filter(action='buy', product_id=''),
    filters.ChatTypeFilter(aiogram.types.ChatType.PRIVATE))
async def subcategory_products(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    category_id = int(callback_data['category_id'])
    subcategory_id = callback_data['subcategory_id']
    subcategory_id = int(subcategory_id) if subcategory_id != '' else None
    with db_api.create_session() as session:
        if not queries.check_is_user_exists(session, query.from_user.id):
            raise exceptions.UserNotInDatabase
        products = queries.get_category_products(session, category_id, subcategory_id)
        await responses.products.SubcategoryProductsResponse(
            query, category_id, subcategory_id, products
        )


@dp.callback_query_handler(
    callback_factories.ProductCallbackFactory().filter(action='buy'),
    filters.ChatTypeFilter(aiogram.types.ChatType.PRIVATE)
)
async def product_menu(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    product_id = int(callback_data['product_id'])
    subcategory_id = callback_data['subcategory_id']
    category_id = int(callback_data['category_id'])
    subcategory_id = subcategory_id if subcategory_id != '' else None
    with db_api.create_session() as session:
        if not queries.check_is_user_exists(session, query.from_user.id):
            raise exceptions.UserNotInDatabase
        product = queries.get_product(session, product_id)
        if product.picture is not None:
            product_picture = open(config.PRODUCT_PICTURE_PATH / product.picture, 'rb')
        else:
            product_picture = None
        await responses.products.ProductResponse(
            query, product, product.quantity,
            category_id, subcategory_id, product_picture
        )


@dp.callback_query_handler(
    callback_factories.BuyProductCallbackFactory().filter(quantity='', payment_method=''),
    filters.ChatTypeFilter(aiogram.types.ChatType.PRIVATE))
async def product_quantity(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    with db_api.create_session() as session:
        if not queries.check_is_user_exists(session, query.from_user.id):
            raise exceptions.UserNotInDatabase
    await responses.products.ProductQuantityResponse(
        query, int(callback_data['product_id']), int(callback_data['available_quantity'])
    )


@dp.callback_query_handler(
    callback_factories.BuyProductCallbackFactory().filter(quantity='another', payment_method=''),
    filters.ChatTypeFilter(aiogram.types.ChatType.PRIVATE))
async def own_product_quantity(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    with db_api.create_session() as session:
        if not queries.check_is_user_exists(session, query.from_user.id):
            raise exceptions.UserNotInDatabase
    await product_states.EnterProductQuantity.waiting_quantity.set()
    await dp.current_state().update_data({'callback_data': callback_data})
    await responses.products.AnotherProductQuantityResponse(
        query, int(callback_data['available_quantity'])
    )


@dp.callback_query_handler(
    callback_factories.BuyProductCallbackFactory().filter(payment_method=''),
    filters.ChatTypeFilter(aiogram.types.ChatType.PRIVATE)
)
async def product_quantity(query: aiogram.types.CallbackQuery, callback_data: dict[str: str]):
    with db_api.create_session() as session:
        if not queries.check_is_user_exists(session, query.from_user.id):
            raise exceptions.UserNotInDatabase
    await responses.products.PaymentMethodResponse(
        query, callback_data, crypto_payments=config.PaymentsSettings().crypto_payments
    )


@dp.message_handler(state=product_states.EnterProductQuantity.waiting_quantity)
async def another_product_quantity(message: aiogram.types.Message, state: dispatcher.FSMContext):
    with db_api.create_session() as session:
        if not queries.check_is_user_exists(session, message.from_user.id):
            raise exceptions.UserNotInDatabase
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
                           filters.ChatTypeFilter(aiogram.types.ChatType.PRIVATE))
async def pay_with_qiwi(query: aiogram.types.CallbackQuery):
    await query.message.answer('🚧 Under Development')


@dp.callback_query_handler(callback_factories.BuyProductCallbackFactory().filter(payment_method='yoomoney'),
                           filters.ChatTypeFilter(aiogram.types.ChatType.PRIVATE))
async def pay_with_yoomoney(query: aiogram.types.CallbackQuery):
    await query.message.answer('🚧 Under Development')


@dp.callback_query_handler(callback_factories.BuyProductCallbackFactory().filter(payment_method='minerlock'),
                           filters.ChatTypeFilter(aiogram.types.ChatType.PRIVATE))
async def pay_with_minerlock(query: aiogram.types.CallbackQuery):
    await query.message.answer('🚧 Under Development')


@dp.callback_query_handler(callback_factories.BuyProductCallbackFactory().filter(payment_method='coinpayments'),
                           filters.ChatTypeFilter(aiogram.types.ChatType.PRIVATE))
async def pay_with_coinpayments(query: aiogram.types.CallbackQuery):
    await query.message.answer('🚧 Under Development')


@dp.callback_query_handler(callback_factories.BuyProductCallbackFactory().filter(payment_method='coinbase'),
                           filters.ChatTypeFilter(aiogram.types.ChatType.PRIVATE))
async def pay_with_coinbase(query: aiogram.types.CallbackQuery, callback_data: dict[str: str]):
    with db_api.create_session() as session:
        user = queries.get_user(session, telegram_id=query.from_user.id)
        if user is None:
            raise exceptions.UserNotInDatabase
        product = queries.get_product(session, int(callback_data['product_id']))
        quantity = int(callback_data['quantity'])
        amount = float(quantity * decimal.Decimal(str(product.price)))
        api = coinbase_api.CoinbaseAPI(config.CoinbaseSettings().api_key)
        charge = api.create_charge(product.name, amount, product.description)
        payment_message = await responses.payments.CoinbasePaymentLinkResponse(
            query, amount, quantity, charge['hosted_url'])
        if await api.check_payment(charge):
            sale = queries.add_sale(
                session, user.id, user.username, product.id,
                amount, quantity, payment_type='coinbase')
            product_units = queries.get_not_sold_product_units(session, product.id, quantity)
            with session.begin_nested():
                queries.edit_product_quantity(session, product.id, -quantity)
                for product_unit in product_units:
                    queries.add_sold_product_unit(session, sale.id, product_unit.id)
            session.expunge_all()
            session.commit()
            await responses.payments.PurchaseInformationResponse(
                query, sale.id, product.name, quantity, amount, product_units
            )
            await notifications.NewPurchaseNotification(sale, '🌐 Coinbase', product.name, product_units).send()
        else:
            await responses.payments.FailedPurchaseResponse(payment_message)


@dp.callback_query_handler(callback_factories.BuyProductCallbackFactory().filter(payment_method='balance'),
                           filters.ChatTypeFilter(aiogram.types.ChatType.PRIVATE))
async def pay_with_balance(query: aiogram.types.CallbackQuery, callback_data: dict[str: str]):
    with db_api.create_session() as session:
        product = queries.get_product(session, int(callback_data['product_id']))
        quantity = int(callback_data['quantity'])
        amount = float(quantity * decimal.Decimal(str(product.price)))
        user = queries.get_user(session, telegram_id=int(query.from_user.id))
        if user is None:
            raise exceptions.UserNotInDatabase
        if user.balance >= amount:
            product_units = queries.get_not_sold_product_units(session, product.id, quantity)
            user = queries.get_user(session, telegram_id=query.from_user.id)
            quantity = len(product_units)
            sale = queries.add_sale(
                session, user.id, user.username,
                product.id, amount, quantity, payment_type='balance'
            )
            with session.begin_nested():
                queries.edit_product_quantity(session, product.id, -quantity)
                queries.top_up_balance(session, user.id, -amount)
                for product_unit in product_units:
                    queries.add_sold_product_unit(session, sale.id, product_unit.id)
            session.expunge_all()
            session.commit()
            await responses.payments.PurchaseInformationResponse(
                query, sale.id, product.name, quantity, amount, product_units
            )
            await notifications.NewPurchaseNotification(sale, '💲 Balance', product.name, product_units).send()
        else:
            await responses.payments.NotEnoughBalanceResponse(query)

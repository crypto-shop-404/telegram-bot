import aiogram
from aiogram import filters

import config
import exceptions
import responses.balance
import responses.payments
from keyboards.inline import callback_factories
from loader import dp
from services import db_api
from services.db_api import queries
from services.payments_apis import coinbase_api
from states import balance_states


@dp.message_handler(filters.Text('💲 Balance'))
async def balance(message: aiogram.types.Message):
    with db_api.create_session() as session:
        if not queries.check_is_user_exists(session, message.from_user.id):
            raise exceptions.UserNotInDatabase
        await responses.balance.BalanceResponse(
            message, queries.get_user(session, telegram_id=message.from_user.id).balance
        )


@dp.callback_query_handler(callback_factories.TopUpBalanceCallbackFactory().filter(amount='', payment_method=''))
async def top_up_balance(query: aiogram.types.CallbackQuery, callback_data: dict[str: str]):
    with db_api.create_session() as session:
        if not queries.check_is_user_exists(session, query.from_user.id):
            raise exceptions.UserNotInDatabase
    await responses.balance.BalanceAmountResponse(query)
    await balance_states.TopUpBalance.waiting_for_amount.set()
    await dp.current_state().update_data({'callback_data': callback_data})


@dp.message_handler(state=balance_states.TopUpBalance.waiting_for_amount)
async def balance_amount(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    with db_api.create_session() as session:
        if not queries.check_is_user_exists(session, message.from_user.id):
            raise exceptions.UserNotInDatabase
    if message.text.replace('.', '').isdigit() and '-' not in message.text:
        callback_data = (await state.get_data())['callback_data']
        callback_data['amount'] = message.text
        await state.finish()
        await responses.balance.PaymentMethodResponse(
            message, callback_data=callback_data,
            crypto_payments=config.PaymentsSettings().crypto_payments
        )
    else:
        await responses.balance.IncorrectBalanceAmountResponse(message)


@dp.callback_query_handler(
    callback_factories.TopUpBalanceCallbackFactory().filter(payment_method='coinbase'),
    filters.ChatTypeFilter(aiogram.types.ChatType.PRIVATE)
)
async def top_up_balance_with_coinbase(query: aiogram.types.CallbackQuery, callback_data: dict[str: str]):
    with db_api.create_session() as session:
        user = queries.get_user(session, telegram_id=query.from_user.id)
        if not queries.check_is_user_exists(session, query.from_user.id):
            raise exceptions.UserNotInDatabase
        amount = float(callback_data['amount'])
        api = coinbase_api.CoinbaseAPI(config.CoinbaseSettings().api_key)
        charge = api.create_charge('Balance', amount)
        payments_message = await responses.payments.CoinbasePaymentBalanceResponse(
            query, amount, charge['hosted_url']
        )
        if await api.check_payment(charge):
            queries.top_up_balance(session, user.id, amount)
            await responses.balance.SuccessBalanceRefillResponse(query, amount)
        else:
            queries.top_up_balance(session, user.id, amount)
            await responses.payments.FailedPurchaseResponse(payments_message)

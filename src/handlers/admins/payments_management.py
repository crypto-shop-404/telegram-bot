import aiogram.types
from aiogram import filters, dispatcher

import config
import responses.payments_management
from filters import is_admin
from keyboards.inline import callback_factories
from loader import dp
from services.payments_apis import coinbase_api
from states import payments_management_states


@dp.message_handler(filters.Text('💳 Payment Management'), is_admin.IsUserAdmin())
async def payments_management(message: aiogram.types.Message):
    await responses.payments_management.PaymentsManagementResponse(message)


@dp.message_handler(filters.Text('🌐 Coinbase'), is_admin.IsUserAdmin())
async def coinbase_management(message: aiogram.types.Message):
    await responses.payments_management.CoinbaseManagementResponse(message)


@dp.callback_query_handler(callback_factories.PaymentSystemCallbackFactory().filter(
    system='coinbase', action='check'), is_admin.IsUserAdmin()
)
async def check_coinbase(query: aiogram.types.CallbackQuery):
    if coinbase_api.CoinbaseAPI(config.CoinbaseSettings().api_key).check():
        await responses.payments_management.PaymentSystemIsValid(query)
    else:
        await responses.payments_management.PaymentSystemIsNotValid(query)


@dp.callback_query_handler(callback_factories.PaymentSystemCallbackFactory().filter(
    system='coinbase', action='change_api_key'), is_admin.IsUserAdmin()
)
async def chane_api_key(query: aiogram.types.CallbackQuery):
    await responses.payments_management.ChangeCoinbaseAPIKeyResponse(query)
    await payments_management_states.ChangeCoinbaseData.waiting_api_key.set()


@dp.message_handler(
    is_admin.IsUserAdmin(), state=payments_management_states.ChangeCoinbaseData.waiting_api_key
)
async def change_api_key(message: aiogram.types.Message, state: dispatcher.FSMContext):
    await state.finish()
    config.set_env_var('COINBASE_API_KEY', message.text)
    await responses.payments_management.SuccessChangingPaymentsData(message)

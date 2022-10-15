import aiogram.types
from aiogram import dispatcher
from aiogram.dispatcher import filters

import responses.shop_information
from filters import is_admin
from keyboards.inline import callback_factories
from loader import dp
from services import db_api
from services.db_api import queries
from states import shop_info_states


@dp.message_handler(filters.Text('🏪 Shop Information'), is_admin.IsUserAdmin())
async def shop_information(message: aiogram.types.Message):
    await responses.shop_information.ShopInformationResponse(message)


@dp.message_handler(filters.Text('ℹ️ FAQ'), is_admin.IsUserAdmin())
async def faq_handler(message: aiogram.types.Message):
    with db_api.create_session() as session:
        faq = queries.get_faq(session)
        await responses.shop_information.FAQResponse(
            message, faq.value if faq is not None else 'Faq', True
        )


@dp.message_handler(filters.Text('📗 Rules'), is_admin.IsUserAdmin())
async def rules_handler(message: aiogram.types.Message):
    with db_api.create_session() as session:
        rules = queries.get_rules(session)
        await responses.shop_information.RulesResponse(
            message, rules.value if rules is not None else 'Rules', True
        )


@dp.message_handler(filters.Text('👋 Greetings'), is_admin.IsUserAdmin())
async def greetings_handler(message: aiogram.types.Message):
    with db_api.create_session() as session:
        greetings = queries.get_greetings(session)
        await responses.shop_information.GreetingsResponse(
            message, greetings.value if greetings is not None else 'Greetings'
        )


@dp.message_handler(filters.Text('✋ Return'), is_admin.IsUserAdmin())
async def comeback_message_handler(message: aiogram.types.Message):
    with db_api.create_session() as session:
        comeback_message = queries.get_comeback_message(session)
        await responses.shop_information.ComebackMessageResponse(
            message, comeback_message.value if comeback_message is not None else 'Comeback Message'
        )


@dp.callback_query_handler(
    callback_factories.ShopInformationFactory().filter(object='faq', action='edit'), is_admin.IsUserAdmin())
async def edit_faq(query: aiogram.types.CallbackQuery):
    await responses.shop_information.EditShopInformationResponse(query)
    await shop_info_states.EditFAQ.waiting_faq.set()


@dp.message_handler(is_admin.IsUserAdmin(), state=shop_info_states.EditFAQ.waiting_faq)
async def edit_faq(message: aiogram.types.Message, state: dispatcher.FSMContext):
    await state.finish()
    with db_api.create_session() as session:
        queries.edit_faq(session, message.text)
    await responses.shop_information.SuccessShopInformationEditing(message)


@dp.callback_query_handler(
    callback_factories.ShopInformationFactory().filter(object='rules', action='edit'), is_admin.IsUserAdmin())
async def edit_rules(query: aiogram.types.CallbackQuery):
    await responses.shop_information.EditShopInformationResponse(query)
    await shop_info_states.EditRules.waiting_rules.set()


@dp.message_handler(is_admin.IsUserAdmin(), state=shop_info_states.EditRules.waiting_rules)
async def edit_rules(message: aiogram.types.Message, state: dispatcher.FSMContext):
    await state.finish()
    with db_api.create_session() as session:
        queries.edit_rules(session, message.text)
    await responses.shop_information.SuccessShopInformationEditing(message)


@dp.callback_query_handler(
    callback_factories.ShopInformationFactory().filter(object='greetings', action='edit'), is_admin.IsUserAdmin())
async def edit_greetings(query: aiogram.types.CallbackQuery):
    await responses.shop_information.EditShopInformationResponse(query)
    await shop_info_states.EditGreetings.waiting_greetings.set()


@dp.message_handler(is_admin.IsUserAdmin(), state=shop_info_states.EditGreetings.waiting_greetings)
async def edit_greetings(message: aiogram.types.Message, state: dispatcher.FSMContext):
    await state.finish()
    with db_api.create_session() as session:
        queries.edit_greetings(session, message.text)
    await responses.shop_information.SuccessShopInformationEditing(message)


@dp.callback_query_handler(callback_factories.ShopInformationFactory().filter(
    object='comeback_message', action='edit'), is_admin.IsUserAdmin()
)
async def edit_comeback_message(query: aiogram.types.CallbackQuery):
    await responses.shop_information.EditShopInformationResponse(query)
    await shop_info_states.EditComebackMessage.waiting_comeback_message.set()


@dp.message_handler(is_admin.IsUserAdmin(), state=shop_info_states.EditComebackMessage.waiting_comeback_message)
async def edit_comeback_message(message: aiogram.types.Message, state: dispatcher.FSMContext):
    await state.finish()
    with db_api.create_session() as session:
        queries.edit_comeback_message(session, message.text)
    await responses.shop_information.SuccessShopInformationEditing(message)

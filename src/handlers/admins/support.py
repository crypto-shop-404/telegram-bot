import aiogram
from aiogram import dispatcher
from aiogram.dispatcher import filters

import responses.support
from filters import is_admin, is_user_in_db
from keyboards.inline import callback_factories
from loader import dp
from services import db_api
from services.db_api import queries
from states import support_states


@dp.message_handler(filters.Text('👨‍💻 Support'), is_user_in_db.IsUserInDB(), is_admin.IsUserAdmin())
async def support(message: aiogram.types.Message):
    await responses.support.AdminSupportMenuResponse(message)


@dp.message_handler(filters.Text('📗 Active Requests'), is_user_in_db.IsUserInDB(),
                    is_admin.IsUserAdmin(), chat_type='private')
async def open_requests(message: aiogram.types.Message):
    with db_api.create_session() as session:
        requests = queries.get_open_support_requests(session)
        await responses.support.OpenSupportRequestsResponse(message, requests)


@dp.message_handler(filters.Text('📕 Closed Requests'), is_user_in_db.IsUserInDB(),
                    is_admin.IsUserAdmin(), chat_type='private')
async def closed_requests(message: aiogram.types.Message):
    with db_api.create_session() as session:
        requests = queries.get_closed_support_requests(session)
        await responses.support.ClosedSupportRequestsResponse(message, requests)


@dp.callback_query_handler(callback_factories.SupportCallbackFactory().filter(action=''),
                           is_user_in_db.IsUserInDB(), is_admin.IsUserAdmin(), chat_type='private')
async def support_request_menu(query: aiogram.types.CallbackQuery, callback_data: dict[str: str]):
    match callback_data['is_open']:
        case 'yes':
            is_open = True
        case 'no':
            is_open = False
        case _:
            is_open = None
    with db_api.create_session() as session:
        request = queries.get_support_request(session, int(callback_data['request_id']))
        await responses.support.SupportRequestResponse(query, request, is_open=is_open)


@dp.callback_query_handler(callback_factories.SupportCallbackFactory().filter(action='delete'),
                           is_user_in_db.IsUserInDB(), is_admin.IsUserAdmin(), chat_type='private')
async def delete_request(query: aiogram.types.CallbackQuery, callback_data: dict[str: str]):
    with db_api.create_session() as session:
        queries.delete_support_request(session, int(callback_data['request_id']))
        if callback_data['is_open'] == 'yes':
            support_requests = queries.get_open_support_requests(session)
            await responses.support.OpenSupportRequestsResponse(query, support_requests)
        elif callback_data['is_open'] == 'no':
            support_requests = queries.get_closed_support_requests(session)
            await responses.support.ClosedSupportRequestsResponse(query, support_requests)


@dp.callback_query_handler(callback_factories.SupportCallbackFactory().filter(action='close'),
                           is_user_in_db.IsUserInDB(), is_admin.IsUserAdmin(), chat_type='private')
async def close_request(query: aiogram.types.CallbackQuery, callback_data: dict[str: str]):
    with db_api.create_session() as session:
        queries.close_support_request(session, int(callback_data['request_id']))
        if callback_data['is_open'] == 'yes':
            support_requests = queries.get_open_support_requests(session)
            await responses.support.OpenSupportRequestsResponse(query, support_requests)
        elif callback_data['is_open'] == 'no':
            support_requests = queries.get_closed_support_requests(session)
            await responses.support.ClosedSupportRequestsResponse(query, support_requests)


@dp.callback_query_handler(callback_factories.SupportCallbackFactory().filter(action='answer'),
                           is_user_in_db.IsUserInDB(), is_admin.IsUserAdmin(), chat_type='private')
async def answer_request(query: aiogram.types.CallbackQuery, callback_data: dict[str: str]):
    await responses.support.AnswerSupportRequestResponse(query)
    await support_states.AnswerSupportRequest.waiting_answer.set()
    await dp.current_state().update_data({'callback_data': callback_data})


@dp.message_handler(is_user_in_db.IsUserInDB(), is_admin.IsUserAdmin(),
                    state=support_states.AnswerSupportRequest.waiting_answer)
async def answer_request(message: aiogram.types.Message, state: dispatcher.FSMContext):
    callback_data = (await state.get_data())['callback_data']
    with db_api.create_session() as session:
        queries.close_support_request(session, int(callback_data['request_id']))
        if callback_data['is_open'] == 'yes':
            support_requests = queries.get_open_support_requests(session)
            await responses.support.OpenSupportRequestsResponse(message, support_requests)
        elif callback_data['is_open'] == 'no':
            support_requests = queries.get_closed_support_requests(session)
            await responses.support.ClosedSupportRequestsResponse(message, support_requests)

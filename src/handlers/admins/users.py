import decimal

import aiogram
from aiogram import filters, dispatcher

import responses.users
from filters import is_admin
from keyboards.inline import callback_factories
from keyboards.inline import common_keybords
from loader import dp, bot
from services import db_api
from services.db_api import queries
from states import users_states


@dp.message_handler(filters.Text('🙍‍♂ Users'), is_admin.IsUserAdmin())
async def users(message: aiogram.types.Message):
    with db_api.create_session() as session:
        total_balance, page_size = queries.get_total_balance(session), 10
        await responses.users.UsersResponse(
            message, queries.get_users(session, page_size + 1), total_balance,
            page_size=page_size
        )


@dp.callback_query_handler(
    callback_factories.UserCallbackFactory().filter(filter='', id='', action=''), is_admin.IsUserAdmin()
)
async def users(query: aiogram.types.CallbackQuery, callback_data: dict):
    with db_api.create_session() as session:
        total_balance = queries.get_total_balance(session)
        page, page_size = int(callback_data['page']), 10
        await responses.users.UsersResponse(
            query, queries.get_users(session, page_size + 1, page * page_size),
            total_balance, page=page, page_size=page_size
        )


@dp.callback_query_handler(
    callback_factories.UserCallbackFactory().filter(id='', action='search'), is_admin.IsUserAdmin()
)
async def search_users(query: aiogram.types.CallbackQuery):
    await responses.users.SearchUserResponse(query)
    await users_states.SearchUsersStates.waiting_identifiers.set()


@dp.message_handler(is_admin.IsUserAdmin(), state=users_states.SearchUsersStates.waiting_identifiers)
async def search_users(message: aiogram.types.Message, state: dispatcher.FSMContext):
    await state.finish()
    usernames, ids = [], []
    page, page_size = 0, 10
    total_balance = decimal.Decimal('0')
    for identifier in message.text.split():
        if identifier.isdigit():
            ids.append(int(identifier))
        else:
            usernames.append(identifier.lower())
    with db_api.create_session() as session:
        user_list = queries.get_users(session, page_size + 1, page_size * page, usernames, ids)
        for user in user_list:
            total_balance += decimal.Decimal(str(user.balance))
        filter_message = await responses.users.FoundUsersResponse(message)
        await responses.users.UsersResponse(
            message, user_list, float(total_balance), filter_message.message_id, page, page_size
        )


@dp.callback_query_handler(
    callback_factories.UserCallbackFactory().filter(id='', action=''), is_admin.IsUserAdmin()
)
async def users(query: aiogram.types.CallbackQuery, callback_data: dict):
    usernames, ids = [], []
    page, page_size = int(callback_data['page']), 10
    total_balance = decimal.Decimal('0')
    filter_message = await bot.edit_message_reply_markup(
        query.message.chat.id, int(callback_data['filter']), reply_markup=common_keybords.MockKeyboard()
    )
    await filter_message.delete_reply_markup()
    for identifier in filter_message.text.split(': ', 1)[-1].split():
        if identifier.isdigit():
            ids.append(int(identifier))
        else:
            usernames.append(identifier.lower())
    with db_api.create_session() as session:
        user_list = queries.get_users(session, page_size + 1, page_size * page, usernames, ids)
        for user in user_list:
            total_balance += decimal.Decimal(str(user.balance))
        await responses.users.UsersResponse(
            query, user_list, float(total_balance), query.message.message_id, page, page_size
        )


@dp.callback_query_handler(
    callback_factories.UserCallbackFactory().filter(action='manage'), is_admin.IsUserAdmin()
)
async def user_menu(query: aiogram.types.CallbackQuery, callback_data: dict[str: str]):
    with db_api.create_session() as session:
        user = queries.get_user(session, int(callback_data['id']))
        number_of_orders = queries.count_user_orders(session, user.id)
        await responses.users.UserResponse(query, user, number_of_orders, callback_data)


@dp.callback_query_handler(
    callback_factories.UserCallbackFactory().filter(action='ban', is_confirmed=''), is_admin.IsUserAdmin()
)
async def ban_user(query: aiogram.types.CallbackQuery, callback_data: dict[str: str]):
    with db_api.create_session() as session:
        user = queries.get_user(session, int(callback_data['id']))
        await responses.users.BanUserAlertResponse(query, user, callback_data)


@dp.callback_query_handler(
    callback_factories.UserCallbackFactory().filter(action='ban'), is_admin.IsUserAdmin()
)
async def ban_user(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    with db_api.create_session() as session:
        user_id = int(callback_data['id'])
        if callback_data['is_confirmed'] == 'yes':
            user = queries.ban_user(session, user_id)
        else:
            user = queries.get_user(session, user_id)
        number_of_orders = queries.count_user_orders(session, user.id)
        await responses.users.UserResponse(query, user, number_of_orders, callback_data)


@dp.callback_query_handler(
    callback_factories.UserCallbackFactory().filter(action='unban', is_confirmed=''), is_admin.IsUserAdmin()
)
async def unban_user(query: aiogram.types.CallbackQuery, callback_data: dict[str: str]):
    with db_api.create_session() as session:
        user = queries.get_user(session, int(callback_data['id']))
        await responses.users.UnbanUserAlertResponse(query, user, callback_data)


@dp.callback_query_handler(
    callback_factories.UserCallbackFactory().filter(action='unban'), is_admin.IsUserAdmin()
)
async def unban_user(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    with db_api.create_session() as session:
        user_id = int(callback_data['id'])
        if callback_data['is_confirmed'] == 'yes':
            user = queries.unban_user(session, user_id)
        else:
            user = queries.get_user(session, user_id)
        number_of_orders = queries.count_user_orders(session, user.id)
        await responses.users.UserResponse(query, user, number_of_orders, callback_data)


@dp.callback_query_handler(
    callback_factories.UserCallbackFactory().filter(action='delete', is_confirmed=''), is_admin.IsUserAdmin()
)
async def delete_user(query: aiogram.types.CallbackQuery, callback_data: dict[str: str]):
    with db_api.create_session() as session:
        user = queries.get_user(session, int(callback_data['id']))
        await responses.users.DeleteUserAlert(query, user, callback_data)


@dp.callback_query_handler(
    callback_factories.UserCallbackFactory().filter(action='delete'), is_admin.IsUserAdmin()
)
async def delete_user(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    with db_api.create_session() as session:
        user_id = int(callback_data['id'])
        user = queries.get_user(session, user_id)
        if callback_data['is_confirmed'] == 'yes':
            queries.delete_user(session, user_id)
            total_balance = queries.get_total_balance(session)
            page, page_size = int(callback_data['page']), 10
            success_message = await responses.users.SuccessUserRemovalResponse(query, user)
            await responses.users.UsersResponse(
                success_message, queries.get_users(session, page_size + 1, page * page_size),
                total_balance, page=page, page_size=page_size
            )
        else:
            number_of_orders = queries.count_user_orders(session, user.id)
            await responses.users.UserResponse(query, user, number_of_orders, callback_data)


@dp.callback_query_handler(
    callback_factories.EditUserBalanceCallbackFactory().filter(is_confirmed=''), is_admin.IsUserAdmin()
)
async def edit_balance(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    await responses.users.NewBalanceResponse(query)
    await users_states.EditBalanceStates.waiting_balance.set()
    await dp.current_state().update_data({'callback_data': callback_data})


@dp.message_handler(is_admin.IsUserAdmin(), state=users_states.EditBalanceStates.waiting_balance)
async def enter_new_balance(message: aiogram.types.Message, state: dispatcher.FSMContext):
    if message.text.replace('.', '').isdigit():
        callback_data = (await state.get_data())['callback_data']
        with db_api.create_session() as session:
            user = queries.get_user(session, callback_data['user_id'])
            await responses.users.EditBalanceAlertResponse(
                message, user, message.text, callback_data
            )
            await state.finish()
    else:
        await responses.users.IncorrectBalanceResponse(message)


@dp.callback_query_handler(
    callback_factories.EditUserBalanceCallbackFactory().filter(reason=''), is_admin.IsUserAdmin()
)
async def balance_editing_reason(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    if callback_data['is_confirmed'] == 'yes':
        await responses.users.BalanceEditingReasonResponse(query, callback_data)
    else:
        with db_api.create_session() as session:
            user_id = int(callback_data['user_id'])
            user = queries.get_user(session, user_id)
            await responses.users.UserResponse(
                query, user, queries.count_user_orders(session, user_id)
            )


@dp.callback_query_handler(callback_factories.EditUserBalanceCallbackFactory().filter(), is_admin.IsUserAdmin())
async def edit_balance(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    with db_api.create_session() as session:
        new_balance = float(callback_data['balance'])
        user_id = int(callback_data['user_id'])
        match callback_data['reason']:
            case 'p2p_delivery':
                reason = 'P2P delivery'
            case 'admin_mistake':
                reason = 'Admin mistake'
            case 'refunded_payment':
                reason = 'Refunded payment'
            case _:
                reason = None
        user = queries.get_user(session, user_id)
        if reason is not None:
            await responses.users.SuccessBalanceEditing(query, user, new_balance, reason)
            queries.update_balance(session, user_id, new_balance)
            number_of_orders = queries.count_user_orders(session, user.id)
            await responses.users.UserResponse(query, user, number_of_orders)


@dp.callback_query_handler(
    callback_factories.TopUpUserBalanceCallbackFactory().filter(is_confirmed=''), is_admin.IsUserAdmin()
)
async def top_up_balance(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    await responses.users.NewBalanceResponse(query)
    await users_states.TopUpBalanceStates.waiting_balance.set()
    await dp.current_state().update_data({'callback_data': callback_data})


@dp.message_handler(is_admin.IsUserAdmin(), state=users_states.TopUpBalanceStates.waiting_balance)
async def enter_balance(message: aiogram.types.Message, state: dispatcher.FSMContext):
    if message.text.replace('.', '').isdigit():
        callback_data = (await state.get_data())['callback_data']
        with db_api.create_session() as session:
            user = queries.get_user(session, callback_data['user_id'])
            await responses.users.TopUpBalanceAlertResponse(
                message, user, message.text, callback_data
            )
            await state.finish()
    else:
        await responses.users.IncorrectBalanceResponse(message)


@dp.callback_query_handler(
    callback_factories.TopUpUserBalanceCallbackFactory().filter(payment_method=''), is_admin.IsUserAdmin()
)
async def balance_refill_method(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    if callback_data['is_confirmed'] == 'yes':
        await responses.users.BalanceRefillMethodResponse(query, callback_data)
    else:
        with db_api.create_session() as session:
            user_id = int(callback_data['user_id'])
            user = queries.get_user(session, user_id)
            await responses.users.UserResponse(
                query, user, queries.count_user_orders(session, user_id)
            )


@dp.callback_query_handler(callback_factories.TopUpUserBalanceCallbackFactory().filter(), is_admin.IsUserAdmin())
async def top_up_balance(query: aiogram.types.CallbackQuery, callback_data: dict[str, str]):
    with db_api.create_session() as session:
        balance_delta = decimal.Decimal(callback_data['balance_delta'])
        user_id = int(callback_data['user_id'])
        reason = callback_data['payment_method'].capitalize()
        queries.top_up_balance(session, user_id, balance_delta)
        user = queries.get_user(session, user_id)
        await responses.users.SuccessBalanceRefillResponse(query, user, float(balance_delta), reason)
        number_of_orders = queries.count_user_orders(session, user.id)
        await responses.users.UserResponse(query, user, number_of_orders)

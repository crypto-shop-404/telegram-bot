import datetime

import aiogram

from keyboards.inline import callback_factories


class UserButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, user_id: int, user_tg_id: int, balance: float,
                 registration_date: datetime.date, username: str = None, **callback_data):
        callback_data.pop('@')
        callback_data['action'] = 'manage'
        callback_data['id'] = user_id
        super().__init__(
            text=f'#{user_tg_id} | {username + " | " if username is not None else ""}'
                 f'${balance} | {registration_date}',
            callback_data=callback_factories.UserCallbackFactory().new(**callback_data)
        )


class SearchUsersButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, **callback_data):
        callback_data.pop('@')
        callback_data['action'] = 'search'
        super().__init__('🔎 Search Users', callback_data=callback_factories.UserCallbackFactory().new(
            **callback_data
        ))


class BanUserButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, user_id: int, **callback_data):
        callback_data.pop('@')
        callback_data['action'] = 'ban'
        callback_data['id'] = str(user_id)
        super().__init__(
            text='📛 Ban',
            callback_data=callback_factories.UserCallbackFactory().new(**callback_data)
        )


class UnbanUserButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, user_id: int, **callback_data):
        callback_data.pop('@')
        callback_data['action'] = 'unban'
        callback_data['id'] = str(user_id)
        super().__init__(
            text='🆓 Unban',
            callback_data=callback_factories.UserCallbackFactory().new(**callback_data)
        )


class TopUpBalanceButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, user_id: int):
        super().__init__(
            text='💸 Top Up Balance',
            callback_data=callback_factories.TopUpUserBalanceCallbackFactory().new(
                user_id=user_id, balance_delta='', payment_method='', is_confirmed=''
            )
        )


class EditBalanceButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, user_id: int):
        super().__init__(
            text='⚖️ Edit Balance',
            callback_data=callback_factories.EditUserBalanceCallbackFactory().new(
                user_id=user_id, balance='', reason='', is_confirmed=''
            )
        )


class DeleteUserButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, user_id: int, **callback_data):
        callback_data.pop('@')
        callback_data['action'] = 'delete'
        callback_data['id'] = str(user_id)
        super().__init__(
            text='🫥 Delete User',
            callback_data=callback_factories.UserCallbackFactory().new(**callback_data)
        )


class P2PDeliveryButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, user_id: int, balance: float):
        super().__init__(
            text='🤝 P2P Delivery',
            callback_data=callback_factories.EditUserBalanceCallbackFactory().new(
                user_id, balance=balance, reason='p2p_delivery', is_confirmed='yes'
            )
        )


class AdminMistakeButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, user_id: int, balance: float):
        super().__init__(
            '🫤 Admin Mistake',
            callback_data=callback_factories.EditUserBalanceCallbackFactory().new(
                user_id, balance=balance, reason='admin_mistake', is_confirmed='yes'
            )
        )


class RefundedPaymentButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, user_id: int, balance: float):
        super().__init__(
            '🔄 Refunded Payment',
            callback_data=callback_factories.EditUserBalanceCallbackFactory().new(
                user_id, balance=balance, reason='refunded_payment', is_confirmed='yes'
            )
        )


class CashAppPaymentMethod(aiogram.types.InlineKeyboardButton):
    def __init__(self, user_id: int, balance_delta: float):
        super().__init__(
            '💳 Cashapp',
            callback_data=callback_factories.TopUpUserBalanceCallbackFactory().new(
                user_id, balance_delta=balance_delta, payment_method='cashapp', is_confirmed='yes'
            )
        )


class AnotherPaymentMethod(aiogram.types.InlineKeyboardButton):
    def __init__(self, user_id: int, balance_delta: float):
        super().__init__(
            '💎 Other',
            callback_data=callback_factories.TopUpUserBalanceCallbackFactory().new(
                user_id, balance_delta=balance_delta, payment_method='other', is_confirmed='yes'
            )
        )

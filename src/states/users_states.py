from aiogram.dispatcher.filters import state


class SearchUsersStates(state.StatesGroup):
    waiting_identifiers = state.State()


class EditBalanceStates(state.StatesGroup):
    waiting_balance = state.State()


class TopUpBalanceStates(state.StatesGroup):
    waiting_balance = state.State()

from aiogram.dispatcher.filters import state


class ChangeCoinbaseData(state.StatesGroup):
    waiting_api_key = state.State()

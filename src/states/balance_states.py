from aiogram.dispatcher.filters import state


class TopUpBalance(state.StatesGroup):
    waiting_for_amount = state.State()

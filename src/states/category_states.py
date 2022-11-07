from aiogram.dispatcher.filters import state


class AddCategories(state.StatesGroup):
    waiting_title = state.State()


class AddSubcategories(state.StatesGroup):
    waiting_title = state.State()

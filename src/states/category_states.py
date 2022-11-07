from aiogram.dispatcher.filters import state


class AddCategories(state.StatesGroup):
    waiting_category_name = state.State()


class AddSubcategories(state.StatesGroup):
    waiting_name = state.State()

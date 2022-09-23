from aiogram.dispatcher.filters import state


class AddProduct(state.StatesGroup):
    waiting_name = state.State()
    waiting_description = state.State()
    waiting_picture = state.State()
    waiting_price = state.State()
    waiting_content = state.State()


class EditProductTitle(state.StatesGroup):
    waiting_title = state.State()


class EditProductDescription(state.StatesGroup):
    waiting_description = state.State()


class EditProductPicture(state.StatesGroup):
    waiting_picture = state.State()


class EditProductPrice(state.StatesGroup):
    waiting_price = state.State()


class AddProductUnit(state.StatesGroup):
    waiting_content = state.State()


class EditProductUnit(state.StatesGroup):
    waiting_content = state.State()


class EnterProductQuantity(state.StatesGroup):
    waiting_quantity = state.State()

from aiogram.dispatcher.filters import state


class EditFAQ(state.StatesGroup):
    waiting_faq = state.State()


class EditRules(state.StatesGroup):
    waiting_rules = state.State()


class EditGreetings(state.StatesGroup):
    waiting_greetings = state.State()


class EditComebackMessage(state.StatesGroup):
    waiting_comeback_message = state.State()

from aiogram.dispatcher.filters import state


class MailingStates(state.StatesGroup):
    waiting_newsletter = state.State()

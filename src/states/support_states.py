from aiogram.dispatcher.filters import state


class AddSupportSubject(state.StatesGroup):
    waiting_subject = state.State()


class AddSupportRequest(state.StatesGroup):
    waiting_issue = state.State()


class AnswerSupportRequest(state.StatesGroup):
    waiting_answer = state.State()

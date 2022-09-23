from aiogram.dispatcher.filters import state


class BackupStates(state.StatesGroup):
    waiting_for_backup_period = state.State()
    waiting_for_sending_backup_period = state.State()

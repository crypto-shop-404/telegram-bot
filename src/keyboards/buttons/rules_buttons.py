import aiogram.types


class AcceptRulesButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='✅ Accept')

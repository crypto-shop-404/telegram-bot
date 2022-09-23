import aiogram.types


class GeneralStatisticsButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='📊 General')


class DailyStatisticsButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='📆 Daily')

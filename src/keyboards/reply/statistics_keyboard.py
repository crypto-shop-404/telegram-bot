import aiogram

from keyboards.buttons import statistics_buttons, navigation_buttons


class StatisticsKeyboard(aiogram.types.ReplyKeyboardMarkup):
    def __init__(self):
        super().__init__(row_width=2, resize_keyboard=True)
        self.add(
            statistics_buttons.GeneralStatisticsButton(),
            statistics_buttons.DailyStatisticsButton()
        )
        self.row(navigation_buttons.BackButton())

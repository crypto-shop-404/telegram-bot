import aiogram.types

from keyboards.buttons import backup_buttons, navigation_buttons


class BackupKeyboard(aiogram.types.ReplyKeyboardMarkup):
    def __init__(self):
        super().__init__(row_width=3, resize_keyboard=True)
        self.add(
            backup_buttons.ManualBackupButton(),
            backup_buttons.BackupFullShopButton(),
            backup_buttons.ManageBackupScheduleButton()
        )
        self.add(navigation_buttons.BackButton())


class BackupPeriodKeyboard(aiogram.types.ReplyKeyboardMarkup):
    def __init__(self):
        super().__init__(row_width=3, resize_keyboard=True)
        self.add(
            backup_buttons.BackupEveryHourButton(),
            backup_buttons.BackupEverySixHourButton(),
            backup_buttons.BackupEveryDayButton()
        )
        self.add(navigation_buttons.BackButton())


class SendingBackupPeriodKeyboard(aiogram.types.ReplyKeyboardMarkup):
    def __init__(self):
        super().__init__(row_width=3, resize_keyboard=True)
        self.add(
            backup_buttons.SendBackupEverydayButton(),
            backup_buttons.SendBackupEveryThreeDayButton(),
            backup_buttons.SendBackupEveryWeekButton()
        )
        self.add(navigation_buttons.BackButton())

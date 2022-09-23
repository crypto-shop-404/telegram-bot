import aiogram


class ManualBackupButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__('📀 Manual Backup')


class BackupFullShopButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__('📲 Backup Full Shop')


class ManageBackupScheduleButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__('⏰ Manage Cron')


class BackupEveryHourButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__('⏱ Every Hour')


class BackupEverySixHourButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__('⏱ Every Six Hours')


class BackupEveryDayButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__('⏱ Every 24 Hours')


class SendBackupEverydayButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__('⏱ Everyday')


class SendBackupEveryThreeDayButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__('⏱ Every 3 Days')


class SendBackupEveryWeekButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__('⏱ Every Week')

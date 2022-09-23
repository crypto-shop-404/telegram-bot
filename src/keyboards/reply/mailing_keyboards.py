import aiogram.types

from keyboards.buttons import mailing_buttons, navigation_buttons


class MailingKeyboard(aiogram.types.ReplyKeyboardMarkup):
    def __init__(self):
        super().__init__(resize_keyboard=True)
        self.add(mailing_buttons.CreateNewsletterButton())
        self.row(navigation_buttons.BackButton())

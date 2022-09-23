import aiogram.types

from keyboards.inline import callback_factories


class CreateNewsletterButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='📮 Create Newsletter')


class MarkdownNewsletterButton(aiogram.types.InlineKeyboardButton):
    def __init__(self):
        super().__init__(
            text='Markdown', callback_data=callback_factories.MailingCallbackFactory().new(
                markup='markdown'
            )
        )


class HTMLNewsletterButton(aiogram.types.InlineKeyboardButton):
    def __init__(self):
        super().__init__(
            text='HTML', callback_data=callback_factories.MailingCallbackFactory().new(
                markup='html'
            )
        )


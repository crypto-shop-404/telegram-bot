import aiogram.types

from keyboards.inline import callback_factories


class FAQButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='ℹ️ FAQ')


class RulesButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='📗 Rules')


class GreetingsButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='👋 Greetings')


class ComebackMessageButton(aiogram.types.KeyboardButton):
    def __init__(self):
        super().__init__(text='✋ Return')


class EditFAQButton(aiogram.types.InlineKeyboardButton):
    def __init__(self):
        super().__init__(
            text='📝 Edit', callback_data=callback_factories.ShopInformationFactory().new(
                object='faq', action='edit'
            )
        )


class EditRulesButton(aiogram.types.InlineKeyboardButton):
    def __init__(self):
        super().__init__(
            text='📝 Edit', callback_data=callback_factories.ShopInformationFactory().new(
                object='rules', action='edit'
            )
        )


class EditGreetingsButton(aiogram.types.InlineKeyboardButton):
    def __init__(self):
        super().__init__(
            text='📝 Edit', callback_data=callback_factories.ShopInformationFactory().new(
                object='greetings', action='edit'
            )
        )


class EditComebackMessageButton(aiogram.types.InlineKeyboardButton):
    def __init__(self):
        super().__init__(
            text='📝 Edit', callback_data=callback_factories.ShopInformationFactory().new(
                object='comeback_message', action='edit'
            )
        )

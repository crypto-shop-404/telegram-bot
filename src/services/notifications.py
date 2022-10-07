import abc

import config
from config import AppSettings
from loader import bot
from services.db_api import schemas


class BaseNotification(abc.ABC):
    @abc.abstractmethod
    def send(self, *args):
        pass


class NewUserNotification(BaseNotification):
    def __init__(self, user_id: int, username: str):
        self.__user_id = user_id
        self.__username = username

    async def send(self):
        text = (
                '📱 New user\n'
                '➖➖➖➖➖➖➖➖➖➖\n' +
                ('🙍‍♂ Name: '
                 f'{self.__username}\n' if self.__username else '') +
                f'🆔 ID: {self.__user_id}'
        )
        for user_id in AppSettings().admins_id:
            await bot.send_message(user_id, text)


class NewPurchaseNotification(BaseNotification):
    def __init__(self, sale: schemas.Sale, payment_method: str):
        self.__sale = sale
        self.__payment_method = payment_method

    async def send(self):
        text = self.__get_text()
        product_unit_type = self.__sale.product_unit.type
        product_unit_content = self.__sale.product_unit.content
        if product_unit_type == 'document':
            for user_id in AppSettings().admins_id:
                await bot.send_message(user_id, text)
                await bot.send_document(config.PRODUCT_UNITS_PATH / product_unit_content)
        elif product_unit_content == 'text':
            text += self.__sale.product_unit.content
            for user_id in AppSettings().admins_id:
                await bot.send_message(user_id, text)

    def __get_text(self):
        return (
                '🛒 New purchase\n'
                '➖➖➖➖➖➖➖➖➖➖\n'
                f'🆔 Order Number: {self.__sale.id}\n' +
                (f'🙍‍♂ Customer: @{self.__sale.username}\n' if self.__sale.username is not None else '') +
                f'#️⃣ User ID: {self.__sale.user_id}\n'
                '➖➖➖➖➖➖➖➖➖➖\n'
                f'📙 Product Name: {self.__sale.product_name}\n'
                f'📦 Quantity: {self.__sale.quantity} pc(s).\n'
                f'💰 Amount of purchase: ${self.__sale.amount}.\n'
                '➖➖➖➖➖➖➖➖➖➖\n'
                f'💳 Payment Method: {self.__payment_method}\n'
                '➖➖➖➖➖➖➖➖➖➖\n'
                '📱 Data:\n\n'
        )


class NewSupportRequestNotification(BaseNotification):
    def __init__(self, support_request: schemas.SupportRequest):
        self.__support_request = support_request

    async def send(self):
        text = (
                '👨‍💻 New request\n'
                '➖➖➖➖➖➖➖➖➖➖\n'
                f'🆔 Request number: {self.__support_request.id}\n'
                f'🙍‍♂ User: ' +
                (f'@{self.__support_request.username}\n' if self.__support_request.username is not None else
                 f'{self.__support_request.user_id}\n') +
                '➖➖➖➖➖➖➖➖➖➖\n'
                f'📗 Request subject: {self.__support_request.subject.name}\n'
                '📋 Description:\n\n'
                f'{self.__support_request.issue}'
        )
        for user_id in AppSettings().admins_id:
            await bot.send_message(user_id, text)


class AnsweredSupportRequestNotification(BaseNotification):
    def __init__(self, request_id: int, answer: str):
        self.__request_id = request_id
        self.__answer = answer

    async def send(self, user_id: int):
        text = (
                '✅ Your request was reviewed\n'
                '➖➖➖➖➖➖➖➖➖➖\n'
                f'🆔 Request number: {self.__request_id}\n'
                '📕 Answer:\n\n' + self.__answer
        )
        await bot.send_message(user_id, text)


class ErrorNotification(BaseNotification):
    def __init__(self, error_message: Exception):
        self.__error_message = error_message

    async def send(self):
        text = (
            f"❗ Error During Operation ❗\n"
            f"{self.__error_message}\n\n❗"
            f" The bot will restart automatically."
        )
        for user_id in AppSettings().admins_id:
            await bot.send_message(user_id, text)

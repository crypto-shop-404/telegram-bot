import typing

import aiogram.types

from responses import base


class User(typing.TypedDict):
    id: int
    username: str
    purchase_number: int
    orders_amount: float


class GeneralStatisticsResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message, buyers_number: int, orders_amount: float,
                 sold_products_number: int, active_buyers: list[User]):
        self.__message = message
        self.__buyers_number = buyers_number
        self.__orders_amount = orders_amount
        self.__sold_products_number = sold_products_number
        self.__active_buyers = active_buyers

    async def _send_response(self):
        message_text = (
                f'🙍‍♂ Number of buyers: {self.__buyers_number}\n'
                f'💰 Total Orders: {self.__orders_amount} $.\n'
                '➖➖➖➖➖➖➖➖➖➖\n'
                f'🛒 Number of purchased items: {self.__sold_products_number}\n\n'
                '➖➖➖➖➖➖➖➖➖➖\n'
                '🙍‍♂ Active buyers:\n' +
                '\n'.join([f'#{buyer["id"]}' for buyer in self.__active_buyers]) +
                '➖➖➖➖➖➖➖➖➖➖')
        await self.__message.answer()

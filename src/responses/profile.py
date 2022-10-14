import aiogram.types

from responses import base


class ProfileResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message, user_id: int, username: str | None,
                 purchases_number: int, orders_amount: float, last_purchases: list[tuple[str, int, float]]):
        self.__message = message
        self.__user_id = user_id
        self.__username = username
        self.__purchases_number = purchases_number
        self.__orders_amount = orders_amount
        self.__last_purchases = last_purchases

    async def _send_response(self):
        await self.__message.answer(self.__get_text())

    def __get_text(self) -> str:
        text = (
            f'🙍‍♂ User: {self.__user_id if self.__username is None else "@" + self.__username}\n'
            '➖➖➖➖➖➖➖➖➖➖\n'
            f'🛒 Number of purchases: {self.__purchases_number} pc(s).\n'
            f'💰 Total Amount: {self.__orders_amount} $.\n'
            '➖➖➖➖➖➖➖➖➖➖\n'
            '📱 Last 10 purchases:\n'
        )
        for product_name, quantity, amount in self.__last_purchases:
            text += f'{product_name} | {quantity} pc(s) | ${amount}\n'

        return text

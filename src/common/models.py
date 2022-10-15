import typing


class Buyer(typing.TypedDict):
    telegram_id: int
    username: str | None
    purchase_number: int
    orders_amount: float

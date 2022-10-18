import asyncio
import contextlib

import coinbase_commerce
from coinbase_commerce.api_resources import charge
from coinbase_commerce import error
from services.payments_apis import base_payments_api


class CoinbaseAPI(base_payments_api.BasePaymentAPI):
    def __init__(self, api_key: str):
        self.__client = coinbase_commerce.client.Client(api_key=api_key)

    def create_charge(self, name: str, price: float, description: str = None) -> charge.Charge:
        charge_info = {
            "name": name,
            "description": description,
            "local_price": {
                "amount": price,
                "currency": "USD"
            },
            "pricing_type": "fixed_price"
        }
        return self.__client.charge.create(**charge_info)

    @staticmethod
    async def check_payment(payment: charge.Charge) -> bool:
        while not (status := payment['timeline'][-1]['status']) == 'COMPLETED':
            payment.refresh()
            if status in ('EXPIRED', 'CANCELED', 'UNRESOLVED'):
                if payment['timeline'][-1]['context'] == 'OVERPAID':
                    return True
                return False
            await asyncio.sleep(30)
        return True

    def check(self) -> bool:
        with contextlib.suppress(error.ResourceNotFoundError):
            try:
                self.__client.get()
            except error.AuthenticationError:
                return False
        return True

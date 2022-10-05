from services.payments_apis import base_payments_api


class YooMoneyAPI(base_payments_api.BasePaymentAPI):
    def __init__(self, token: str):
        self.__token = token

    def check(self) -> bool:
        return False

from services.payments_apis import base_payments_api


class QiwiAPI(base_payments_api.BasePaymentAPI):
    def __init__(self, token: str):
        self.__api_token = token

    def check(self) -> bool:
        return False

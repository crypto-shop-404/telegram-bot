import typing

import pydantic

import config
from repositories import base_repository
from services import payments_apis


class PaymentsAPIsRepository(base_repository.BaseRepository):
    def __init__(self, crypto_payments: str = None):
        self.__settings_repository = PaymentsAPIsSettingsRepository()
        self.__apis: dict[str: payments_apis.BasePaymentAPI] = {
            'qiwi': payments_apis.QiwiAPI(self.__settings_repository.get('qiwi').token),
            'yoomoney': payments_apis.YooMoneyAPI(self.__settings_repository.get('yoomoney').token),
            'minerlock': payments_apis.MinerlockAPI(
                self.__settings_repository.get('minerlock').api_id,
                self.__settings_repository.get('minerlock').api_key
            ),
            'coinpayments': payments_apis.CoinPaymentsAPI(
                self.__settings_repository.get('coinpayments').public_key,
                self.__settings_repository.get('coinpayments').secret_key
            ),
            'coinbase': payments_apis.CoinbaseAPI(self.__settings_repository.get('coinbase').api_key),
        }
        if crypto_payments is not None:
            self.__apis['crypto_payments'] = self.__apis[crypto_payments]
            self.__apis.pop('minerlock')
            self.__apis.pop('coinbase')
            self.__apis.pop('coinpayments')
            self.__settings_repository.add(
                'crypto_payments',
                self.__settings_repository.get(
                    crypto_payments
                )
            )

    def get_enabled_apis(self) -> typing.Generator[tuple[str, payments_apis.BasePaymentAPI], None, None]:
        for name, api in self.__apis.items():
            if self.__settings_repository.get(name).is_enabled:
                yield name, api

    def get_valid_apis(self) -> typing.Generator[tuple[str, payments_apis.BasePaymentAPI], None, None]:
        for name, api in self.__apis.items():
            settings = self.__settings_repository.get(name)
            if settings is not None and settings.is_enabled and api.check():
                yield name, api


class PaymentsAPIsSettingsRepository(base_repository.BaseRepository):
    def __init__(self):
        self.__settings = {
            'qiwi': config.QIWISettings(),
            'yoomoney': config.YooMoneySettings(),
            'minerlock': config.MinerlockSettings(),
            'coinpayments': config.CoinpaymentsSettings(),
            'coinbase': config.CoinbaseSettings()
        }

    def get(self, name: str):
        return self.__settings.get(name)

    def add(self, name: str, settings: pydantic.BaseSettings):
        self.__settings[name] = settings

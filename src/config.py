import collections
import os
import pathlib
import typing

import dotenv
import pydantic
import toml


ROOT_DIR = pathlib.Path(os.path.abspath('..'))
DATA_PATH = ROOT_DIR / 'data'
BACKUP_PATH = ROOT_DIR / 'backups'
PRODUCT_PICTURE_PATH = DATA_PATH / 'products' / 'pictures'
PRODUCT_UNITS_PATH = DATA_PATH / 'products' / 'units'
PENDING_PATH = DATA_PATH / 'pending'

dotenv.load_dotenv()


def set_env_var(key: str, value: str) -> None:
    dotenv_file = dotenv.find_dotenv()
    dotenv.set_key(dotenv_file, key, value, quote_mode="never")


class TOMLSettings(collections.UserDict):
    SETTINGS_PATH = pathlib.Path(os.curdir) / 'settings.toml'

    __slots__ = ()

    def __init__(self):
        super().__init__()
        settings_file = open(self.SETTINGS_PATH, 'r')
        self.update(toml.load(settings_file))

    def save(self):
        settings_file = open(self.SETTINGS_PATH, 'w')
        toml.dump(self, settings_file)


class AppSettings(pydantic.BaseSettings):
    __slots__ = ()
    bot_token: str = pydantic.Field(..., env='BOT_TOKEN')
    admins_id: list[int] = pydantic.Field([], env='ADMINS_ID')


class PaymentsSettings(pydantic.BaseSettings):
    __slots__ = ()
    crypto_payments: str = TOMLSettings()['payments']['crypto_payments']


class QIWISettings(pydantic.BaseSettings):
    __slots__ = ()
    payment_method: typing.Literal['nickname', 'number'] = TOMLSettings()['payments']['qiwi']['payment_method']
    is_enabled: bool = TOMLSettings()['payments']['qiwi']['is_enabled']
    number: str = pydantic.Field(None, env='QIWI_NUMBER')
    nickname: str = pydantic.Field(None, env='QIWI_NICKNAME')
    token: str = pydantic.Field(None, env='QIWI_TOKEN')


class YooMoneySettings(pydantic.BaseSettings):
    __slots__ = ()
    number: str = pydantic.Field(None, env='YOOMONEY_NUMBER')
    is_enabled: bool = TOMLSettings()['payments']['yoomoney']['is_enabled']
    token: str = pydantic.Field(None, env='YOOMONEY_TOKEN')


class MinerlockSettings(pydantic.BaseSettings):
    __slots__ = ()
    is_enabled: bool = TOMLSettings()['payments']['minerlock']['is_enabled']
    api_id: int = pydantic.Field(None, env='MINERLOCK_API_ID')
    api_key: str = pydantic.Field(None, env='MINERLOCK_API_KEY')


class CoinpaymentsSettings(pydantic.BaseSettings):
    __slots__ = ()
    is_enabled: bool = TOMLSettings()['payments']['coinpayments']['is_enabled']
    public_key: str = pydantic.Field(None, env='COINPAYMENTS_PUBLIC_KEY')
    secret_key: str = pydantic.Field(None, env='COINPAYMENTS_SECRET_KEY')


class CoinbaseSettings(pydantic.BaseSettings):
    __slots__ = ()
    is_enabled: bool = TOMLSettings()['payments']['coinbase']['is_enabled']
    api_key: str = pydantic.Field(None, env='COINBASE_API_KEY')


class BackupSettings(pydantic.BaseSettings):
    __slots__ = ()
    backup_period: str = TOMLSettings()['backup']['backup_period']
    sending_backup_period: str = TOMLSettings()['backup']['sending_backup_period']
    admin_id: int = pydantic.Field(None, env='ADMIN_ID_FOR_BACKUP_SENDING')

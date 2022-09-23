from collections import OrderedDict
from urllib.parse import urlencode
import asyncio
import hashlib
import hmac
import time

import httpx


class CoinPaymentsAPI:
    api_url = 'https://www.coinpayments.net/api.php'
    api_version = 1

    def __init__(self, public_key: str, private_key: str):
        self.public_key = public_key
        self.private_key = private_key

    async def check_transaction(self, txn_id: str) -> bool:
        while not (await self.get_tx_info(txid=txn_id))['result']['status']:
            await asyncio.sleep(30)
            if (await self.get_tx_info(txid=txn_id))['result']['time_expires'] < time.time():
                return False
        return True

    async def get_basic_info(self) -> dict:
        return await self.send_api_request('get_basic_info')

    async def rates(self, **kwargs) -> dict:
        return await self.send_api_request('rates', **kwargs)

    async def balances(self, **kwargs) -> dict:
        return await self.send_api_request('balances', **kwargs)

    async def get_deposit_address(self, **kwargs) -> dict:
        return await self.send_api_request('get_deposit_address', **kwargs)

    async def create_transaction(self, **kwargs) -> dict:
        return await self.send_api_request('create_transaction', **kwargs)

    async def get_callback_address(self, **kwargs) -> dict:
        return await self.send_api_request('get_callback_address', **kwargs)

    async def get_tx_info_multi(self, **kwargs) -> dict:
        return await self.send_api_request('get_tx_info_multi', **kwargs)

    async def get_tx_info(self, **kwargs) -> dict:
        return await self.send_api_request('get_tx_info', **kwargs)

    async def get_tx_ids(self, **kwargs) -> dict:
        return await self.send_api_request('get_tx_ids', **kwargs)

    async def create_transfer(self, **kwargs) -> dict:
        return await self.send_api_request('create_transfer', **kwargs)

    async def create_withdrawal(self, **kwargs) -> dict:
        return await self.send_api_request('create_withdrawal', **kwargs)

    async def create_mass_withdrawal(self, **kwargs) -> dict:
        return await self.send_api_request('create_mass_withdrawal', **kwargs)

    async def convert(self, **kwargs) -> dict:
        return await self.send_api_request('convert', **kwargs)

    async def get_withdrawal_history(self, **kwargs) -> dict:
        return await self.send_api_request('get_withdrawal_history', **kwargs)

    async def get_withdrawal_info(self, **kwargs) -> dict:
        return await self.send_api_request('get_withdrawal_info', **kwargs)

    async def get_conversion_info(self, **kwargs) -> dict:
        return await self.send_api_request('get_conversion_info', **kwargs)

    async def send_api_request(self, command: str, **kwargs) -> dict:
        params = self._build_params(command, **kwargs)
        signature = self._build_signature(params)
        headers = {'HMAC': signature,
                   'Content-Type': 'application/x-www-form-urlencoded'}
        async with httpx.AsyncClient() as session:
            return (await session.post(self.api_url,
                                       params=params,
                                       headers=headers)).json()

    def _build_params(self, command: str, **kwargs) -> str:
        kwargs: dict
        base_params = [('version', self.api_version),
                       ('key', self.public_key),
                       ('cmd', command),
                       ('format', 'json')]
        return urlencode(OrderedDict(base_params + sorted(kwargs.items())))

    def check_signature(self, data: bytes | str, signature: str) -> bool:
        actual_signature = self._build_signature(data)
        return actual_signature == signature

    def _build_signature(self, params: bytes | str) -> str:
        if not isinstance(params, bytes):
            params = bytearray(params, 'utf-8')

        byte_private_key = bytearray(self.private_key, 'utf-8')

        return hmac.new(byte_private_key, params, hashlib.sha512).hexdigest()

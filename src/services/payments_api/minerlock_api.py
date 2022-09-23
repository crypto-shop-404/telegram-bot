import asyncio

import httpx


class MinerlockAPI:
    def __init__(self, uid: int, api_key: str):
        self.uid = uid
        self.api_key = api_key
        self.url = url = 'https://api.minerlock.com'
        self.token = self.get_token()

    def get_token(self) -> str:
        response = httpx.get(f'{self.url}/?action=get-token&uid={self.uid}&key={self.api_key}')
        return response.json()['token']

    def get_cryptocurrencies_list(self) -> list[str]:
        return [currency for currency in self.get_currencies().json()['currencies'] if currency != 'USD']

    def get_currencies(self, usd_amount: int = 100) -> httpx.Response:
        return httpx.get(f'{self.url}?action=get-currencies&cost={usd_amount}&token={self.token}')

    def get_wallet_address(self, usd_amount: float, crypto_currency: str) -> httpx.Response:
        return httpx.get(f'{self.url}?action=get-wallet&cost={usd_amount}&token={self.token}&crypto={crypto_currency}')

    def get_status(self) -> httpx.Response:
        return httpx.get(f'{self.url}/?action=get-status&token={self.token}')

    async def check_status(self) -> bool:
        while self.get_status():
            await asyncio.sleep(30)
        return False

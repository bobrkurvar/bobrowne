import aiohttp
from app.core.config import load_config
from pathlib import Path

class NonExistentCurrency(Exception):
    pass

path = Path(r'C:\project1\.env')
conf = load_config(path)
api_key = str(conf.CURRENCY_API_KEY)

class ExternalAPI:
    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.url = 'https://api.apilayer.com/currency_data/'
        self._cur_list = None
        self._access_currencies = None

    @property
    async def cur_list(self):
        if self._cur_list is None:
            async with self.session.get(self.url+'list', headers={'apikey': api_key}) as resp:
                print("why?")
                json_resp = await resp.json()
                self._cur_list = dict(json_resp)
        return self._cur_list

    @property
    def access_currencies(self):
        if not self._access_currencies:
            print("what?")
            self._access_currencies = self._cur_list['currencies'].keys()
        return self._access_currencies

    async def convert(self, amount: float = 1, to: str = 'RUB', _from: str = 'USD'):
        if to not in self.access_currencies or _from not in self.access_currencies:
            raise NonExistentCurrency
        async with self.session.get(self.url+'convert', headers={'apikey': api_key}, params={"from": _from, "to": to, "amount": amount}) as resp:
            return await resp.json()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

if __name__ == "__main__":
    import asyncio
    async def main():
        async with ExternalAPI() as ex:
            print(await ex.cur_list)
            print(await ex.cur_list)
            print(await ex.convert())
            print(await ex.convert())

    asyncio.run(main())


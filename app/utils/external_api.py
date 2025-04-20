import aiohttp
from app.core.config import load_config
from pathlib import Path

class NonExistentCurrency(Exception):
    pass

path = Path(r'C:\project1\.env')
conf = load_config(path)
api_key = conf.CURRENCY_API_KEY

class ExternalAPI:
    def __init__(self):
        self.session = None
        self.url = 'https://api.apilayer.com/currency_data/'
        self._cur_list = None

    @property
    async def cur_list(self):
        if self._cur_list is None:
            async with self.session.get(self.url+'list', headers={'apikey': api_key}) as resp:
                json_resp = await resp.json()
                self._cur_list = json_resp
        return self._cur_list

    async def convert(self, amount: float = 1, to: str = 'RUB', _from: str = 'USD'):
        access_currencies = (await self.cur_list).get("currencies").keys()
        if to not in access_currencies or _from not in access_currencies:
            raise NonExistentCurrency
        async with self.session.get(self.url+'convert', headers={'apikey': api_key}, params={"from": _from, "to": to, "amount": amount}) as resp:
            return await resp.json()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
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


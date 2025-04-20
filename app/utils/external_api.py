import aiohttp
from app.core.config import load_config
from pathlib import Path
import asyncio
from app.utils.schemas import Currency

path = Path(r'C:\project1\.env')
conf = load_config(path)
api_key = str(conf.CURRENCY_API_KEY)

class ExternalAPI:
    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.url = 'https://api.apilayer.com/currency_data/'
        self._cur_list = None

    @property
    async def cur_list(self):
        if not self._cur_list:
            async with self.session.get(self.url+'list', headers={'apikey': api_key}) as resp:
                self._cur_list = await resp.json()
        return self._cur_list


    async def convert(self, amount: float = 1, to: str = 'RUB', _from: str = 'USD'):
        async with self.session.get(self.url+'convert', headers={'apikey': api_key}, params={"from": _from, "to": to, "amount": amount}) as resp:
            return await resp.json()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

async def main():
    async with ExternalAPI() as ex:
        r = await ex.cur_list
        print(r)

asyncio.run(main())


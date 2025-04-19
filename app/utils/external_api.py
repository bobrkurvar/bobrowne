import aiohttp

class ExternalAPI:
    def __init__(self):
        self.client = aiohttp.ClientSession
import aiohttp
import asyncio
import logging
import time
from math import ceil
from json import loads



class HTTPResponse:
    def __init__(self, request, text):
        self._request = request
        self._text = text

    @staticmethod
    async def make(request):
        return HTTPResponse(
            request,
            await request.text()
        )

    async def json(self):
        return loads(self._text)

    def raise_for_status(self):
        if self._request.status > 399:
            raise Exception(f"Request failed with status code {self._request.status}")

    @property
    def status(self):
        return self._request.status

    
    async def text(self):
        return self._text


class TwitchHTTP:
    def __init__(self, bot):
        self.aiohttp = aiohttp.ClientSession()

        self.base = "https://api.twitch.tv/helix"
        self.bot = bot
        self.logger = logging.getLogger("http")
        self.token = {}
        self.config = {
            "client_id": bot.config['client_id'],
            "client_secret": bot.config['client_secret'],
            "grant_type": "client_credentials"
        }

    @property
    def default_headers(self):
        return {
            "Accept": "application/vnd.twitchtv.v5+json",
            "Authorization": f"Bearer {self.token.get('access_token')}",
            "Client-ID": self.config["client_id"]
        }

    async def get_bearer_token(self):
        params = self.config
        async with self.aiohttp.post("https://id.twitch.tv/oauth2/token", params=params) as req:
            if req.status > 399:
                self.logger.exception("Error code {} while trying to obtain bearer token".format(req.status))
                self.logger.fatal("%s", await req.text())
                self.token = {}
            
            token = await req.json()
            try:
                token["expires_in"] += time.time()
            except KeyError:
                self.logger.warning("Failed to set token expiration time")
            
            self.logger.info("Obtained access token {}".format(token["access_token"]))
            self.token = token

    async def get(self, url, params=None, v5=False):
        if self.token.get("expires_in", 0) <= time.time() + 1 or not self.token:
            await self.get_bearer_token()
        
        async with self.aiohttp.get(
            f"{'https://api.twitch.tv/kraken' if v5 else self.base}{url}",
            headers=self.default_headers,
            params=params
        ) as req:
            self.logger.debug("GET {}{} {}".format(req.url.host, req.url.path, req.status))
            if req.status > 399:
                self.logger.fatal("%s", await req.text())

            if int(req.headers.get("RateLimit-Remaining", 99)) <= 5 and req.status == 200:
                reset = float(req.headers.get("RateLimit-Reset", time.time()))
                wait = ceil(reset - time.time() + 0.5)
                self.logger.warning("Ratelimit bucket exhausted, waiting {}".format(wait))
                await asyncio.sleep(wait)
            
            return await HTTPResponse.make(req)
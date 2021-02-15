import aiohttp
from datetime import datetime

import discord
from discord.ext import commands

from Cogs import Config




class API(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    
    async def get_bearer_token(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://id.twitch.tv/oauth2/token",
                params={
                    "client_id": Config.CLIENT_ID,
                    "client_secret": Config.CLIENT_SECRET,
                    "grant_type": "client_credentials"
                },
            ) as req:
                try:
                    data = await req.json()
                except aiohttp.ContentTypeError:
                    data = {}
                
                if req.status == 200:
                    pass
                elif req.status == 400 and data.get("message") == "invalid client":
                    print("Invalid Client ID")
                elif req.status == 403 and data.get("message") == "invalid client secret":
                    print("Invalid Client Secret")
                elif "message" in data:
                    print("Request failed with status code {} and error message {}".format(str(req.status), data["message"]))
                else:
                    print(f"Request failed with status code {req.status}")
                
                if req.status != 200:
                    return
            
            self.api_cache = data
            self.api_cache["expires_at"] = datetime.utcnow().timestamp() + data.get("expires_in")



    async def maybe_new_token(self) -> None:
        if self.api_cache:
            if self.api_cache["expires_at"] - datetime.utcnow().timestamp() >= 60:
                await API.get_bearer_token(self=self)




def setup(bot):
    bot.add_cog(API(bot))
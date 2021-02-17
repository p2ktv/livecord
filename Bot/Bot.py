import asyncio

import discord
from discord.ext import commands
from discord.ext.commands import AutoShardedBot

from Twitch import Twitch
from Cogs.API import API
from Cogs import Config


cogs = [
    "API",
    "Task"
]



class TwitchBot(AutoShardedBot):
    READY = False
    api_cache = dict()
    streams = Config.STREAMERS
    sent = []
    def __init__(self, *args, loop=None, **kwargs):
        super().__init__(*args, loop=loop, **kwargs)

    
    async def _run_event(self, coro, event_name, *args, **kwargs):
        while not self.READY and event_name != "on_ready":
            await asyncio.sleep(0.3)
        await super()._run_event(coro, event_name, *args, **kwargs)


    async def on_ready(self):
        if not self.READY:
            await Twitch.init(self)
            await API.get_bearer_token(self)
            for cog in cogs:
                try:
                    self.load_extension("Cogs.{}".format(cog))
                except Exception as e:
                    print("Failed to load cog {}: \n{}".format(cog, e))

            print("Ready as {} ({})".format(self.user, self.user.id))
            self.READY = True
        else:
            pass
        
      
    def run(self):
        try:
            self.remove_command("help")
            super().run(Config.TOKEN, reconnect=True)
        except Exception as e:
            print("Error in run() method, abording! \n{}".format(e))

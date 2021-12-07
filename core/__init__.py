import asyncio
import platform
import time
import traceback
from tabulate import tabulate

import discord
from discord.ext.commands import AutoShardedBot

from utils import TwitchHTTP, Mongo, handle_notifications


plugins = [
    "meta",
    "twitch",
    "notifications"
    #"audio"
]

_ascii = r"""
  _      _                             _ 
 | |    (_)                           | |
 | |     ___   _____  ___ ___  _ __ __| |
 | |    | \ \ / / _ \/ __/ _ \| '__/ _` |
 | |____| |\ V /  __/ (_| (_) | | | (_| |
 |______|_| \_/ \___|\___\___/|_|  \__,_|
"""



class Livecord(AutoShardedBot):
    READY = False
    def __init__(self, config):
        super().__init__(
            command_prefix="!!", case_insensitive=True, max_messages=1000,
            intents=discord.Intents.all(), chunk_guilds_at_startup=True
        )
        
        self.notif_cache = {}
        self.sent_notification = []
        self.loop.create_task(handle_notifications(self))
        self.config = config
        self.color = 0x6441a5
        self.emotes = {
            "arrow": "<:arrow:836558825481568296>",
            "twitch": "<:twitch:836726608332193884>"
        }
        self.uptime = None
        self.twitch_http = TwitchHTTP(self)
        self.db = Mongo(self)


    
    async def _run_event(self, coro, event_name, *args, **kwargs):
        while not self.READY and event_name != "on_ready":
            await asyncio.sleep(0.3)
        await super()._run_event(coro, event_name, *args, **kwargs)


    async def on_ready(self):
        if not self.READY:
            for plugin in plugins:
                try:
                    self.load_extension("plugins.{}".format(plugin))
                except Exception as e:
                    print("Failed to load plugin {}: \n{}".format(plugin, e))

            print(_ascii)
            table_rows = [
                ["discord.py", f"v{discord.__version__}"],
                ["python", f"v{platform.python_version()}"],
                ["system", f"{platform.system()} v{platform.version()}"],
                ["discord user", f"{self.user} (id: {self.user.id})"],
                ["guilds", len(self.guilds)],
                ["users", len(self.users)],
                ["shard ids", getattr(self, "shard_ids", "None")]
            ]
            print("\n" + tabulate(table_rows))
            self.uptime = time.time()
            await self.change_presence(activity=discord.Streaming(name="!!help", url="https://twitch.tv/ezzztv"))
            self.READY = True
        else:
            pass


    async def on_guild_join(self, guild: discord.Guild):
        if len([x for x in self.db.notifications.find({"id": f"{guild.id}"})]) == 0:
            self.db.notifications.insert_one({
                "id": f"{guild.id}",
                "notifications": []
            })

    
    async def on_guild_remove(self, guild: discord.Guild):
        if len([x for x in self.db.notifications.find({"id": f"{guild.id}"})]) == 1:
            self.db.notifications.delete_one({"id": f"{guild.id}"})
        
      
    def run(self):
        try:
            self.remove_command("help")
            super().run(self.config['token'], reconnect=True)
        except Exception:
            e = traceback.format_exc()
            print("Error in run() method, aborting! \n{}".format(e))

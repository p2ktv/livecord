import asyncio
import discord
from discord.ext import commands

from Cogs.API import API
from Cogs import Config
from Twitch.Twitch import noti_channel, get_twitch_data



async def send_msg(c, stream, icon):
    embed = discord.Embed(color=0x6441a5, description="[{}](https://twitch.tv/{})".format(stream["title"], c.lower()))

    embed.set_author(name="{}".format(c), icon_url=icon)
    embed.set_thumbnail(url=icon)
    embed.set_image(url="https://static-cdn.jtvnw.net/previews-ttv/live_user_{}-{}x{}.jpg".format(c.lower(), 440, 248))
    embed.add_field(name="Category/Game", value=stream["game_name"], inline=True)

    await noti_channel.send(content=str(Config.MESSAGE).format(streamer=c, lower=c.lower()), embed=embed)


    
class Task(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.check_channels())


    async def check_channels(self):
        await asyncio.sleep(60) # 60 sec cooldown

        if len(self.bot.streams) < 1:
            return # we don't want to check anything if the channel list is empty

        await API.maybe_new_token(self.bot) # check if we need a new token

        for c in self.bot.streams:
            channel, stream, icon = await get_twitch_data(c)
            if channel is not None: 
                if not c.lower() in self.bot.sent():
                    await send_msg(c, stream, icon)
                    self.bot.sent.append(c.lower())
                else:
                    pass
            else:
                if c.lower() in self.bot.sent():
                    self.bot.sent.remove(c.lower())
                else:
                    pass



def setup(bot):
    bot.add_cog(Task(bot))

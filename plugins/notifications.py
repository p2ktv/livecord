import discord
from discord.ext import commands

import re

from utils import get_notifs



class Notifications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_regex = re.compile(f'^\w+$')

    
    @commands.group()
    async def nf(self, ctx):
        if ctx.invoked_subcommand is None:
            e = discord.Embed(
                color=self.bot.color,
                title="Help - Notifications",
                description="``nf add <streamer> <channel> <message>`` - Adds a notification \n``nf remove <streamer>`` - Removes a notification \n``nf show`` -  List of all notifications"
            )
            await ctx.send(embed=e)


    @nf.command()
    @commands.has_permissions(ban_members=True)
    async def add(self, ctx, streamer: str, channel: discord.TextChannel, *, message: str = None):
        streamer = streamer.split("/")[-1].lower()
        if self.user_regex.match(streamer) is None:
            return await ctx.send("This doesn't look like a valid user")
        if message is None:
            message = "<https://twitch.tv/{}> is now streaming!".format(streamer)
        notifs = await get_notifs(self.bot, ctx.guild.id)
        if streamer in [x["user"] for x in notifs]:
            return await ctx.send("A notification for this streamer already exists")
        if len(message) > 1800:
            return await ctx.send("That message is a bit too long")
        notifs.append({
            "user": streamer,
            "channel": channel.id,
            "message": message
        })
        self.bot.db.notifications.update(
            {
                "id": f"{ctx.guild.id}",
            },
            {
                "$set": {
                    "notifications": notifs
                }
            },
            upsert=False,
            multi=False
        )
        self.bot.notif_cache[f"{ctx.guild.id}"] = notifs
        await ctx.send("Added a notification for ``{}``!".format(streamer))


    @nf.command()
    @commands.has_permissions(ban_members=True)
    async def remove(self, ctx, streamer: str):
        streamer = streamer.split("/")[-1].lower()
        if self.user_regex.match(streamer) is None:
            return await ctx.send("This doesn't look like a valid user")
        notifs = await get_notifs(self.bot, ctx.guild.id)
        if streamer not in [x["user"] for x in notifs]:
            return await ctx.send("A notification for this streamer doesn't exist")
        notifs = [x for x in notifs if not (x["user"] == streamer)]
        self.bot.db.notifications.update(
            {
                "id": f"{ctx.guild.id}",
            },
            {
                "$set": {
                    "notifications": notifs
                }
            },
            upsert=False,
            multi=False
        )
        self.bot.notif_cache[f"{ctx.guild.id}"] = notifs
        await ctx.send("Removed notification for ``{}``!".format(streamer))


    @nf.command()
    @commands.has_permissions(ban_members=True)
    async def show(self, ctx):
        notifs = await get_notifs(self.bot, ctx.guild.id)
        if len(notifs) == 0:
            return await ctx.send("There aren't any notifications for this server")
        
        e = discord.Embed(
            color=self.bot.color,
            title="Streamer Notifications",
            description="Notification count: {}".format(len(notifs))
        )
        for n in notifs:
            e.add_field(
                name="{}".format(n['user']),
                value="• <#{}> \n• {}".format(n['channel'], n['message']),
                inline=False
            )
        await ctx.send(embed=e)
        


def setup(bot): bot.add_cog(Notifications(bot))
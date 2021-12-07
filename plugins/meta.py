import discord
from discord.ext import commands

import time
import sys



class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="help")
    async def _help(self, ctx):
        p = ctx.prefix
        e = discord.Embed(
            color=self.bot.color,
            title="Livecord Help",
            description=f"{self.bot.emotes['arrow']} Type ``{p}commands`` for a full list of commands"
        )
        e.set_thumbnail(url=self.bot.user.avatar_url)
        e.add_field(
            name="Links",
            value="**[GitHub](https://github.com/xezzz/Live)** · **[Twitter](https://twitter.com/xezzz_)**",
            inline=False
        )
        e.set_footer(text="livecord")
        await ctx.send(embed=e)


    @commands.command(name="commands")
    async def _commands(self, ctx):
        e = discord.Embed(
            color=self.bot.color,
            title="Command List",
            description="All commands start with **!!**. \n• Specific commands require certain parameters. \n• When typing commands, do not include ``< >`` around paramaters."
        )
        e.add_field(
            name="General",
            value="```\n{}\n```".format("\n".join(["help", "info", "ping", "commands"])),
            inline=False
        )
        e.add_field(
            name="Twitch",
            value="```\n{}\n```".format("\n".join(["clips game <game>", "clips trending", "clips user <user>", "user <user>"])),
            inline=False
        )
        e.add_field(
            name="Notifications",
            value="```\n{}\n```".format("\n".join(["nf add <streamer> <channel> <message>", "nf remove <streamer>", "nf show"])),
            inline=False
        )
        e.set_footer(text="livecord")
        await ctx.send(embed=e)


    @commands.command()
    async def ping(self, ctx):
        t = time.time()
        await ctx.trigger_typing()
        t2 = round((time.time() - t) * 1000)
        await ctx.send("Pong! {}ms".format(t2))

    def get_uptime(self, uptime):
        t = time.gmtime(time.time() - uptime)
        return f"{t.tm_mday - 1} days, {t.tm_hour} hours, and {t.tm_min} minutes"

    @commands.command()
    async def info(self, ctx):
        e = discord.Embed(
            color=self.bot.color,
            title=f"{self.bot.emotes['twitch']} Livecord Stats"
        )
        e.add_field(
            name="Uptime",
            value=self.get_uptime(self.bot.uptime),
            inline=False,
        )
        e.add_field(
            name="Version",
            value="· Python: {} \n· discord.py {}".format(sys.version.split(' ')[0], discord.__version__),
            inline=True
        )
        e.add_field(
            name="Counts",
            value="· Guilds: {} \n· Members: {} \n· Channels: {}".format(
                len(self.bot.guilds), 
                sum([len(x.members) for x in self.bot.guilds]), 
                sum([len(x.text_channels) + len(x.voice_channels) for x in self.bot.guilds])
            ),
            inline=True
        )
        e.set_footer(text="livecord")
        await ctx.send(embed=e)


    @commands.command(name="reload")
    @commands.is_owner()
    async def _reload(self, ctx, plugin: str):
        plugin = plugin.replace(plugin[0], plugin[0].upper(), 1)
        try:
            self.bot.unload_extension("plugins.{}".format(plugin))
            self.bot.load_extension("plugins.{}".format(plugin))
        except Exception as ex:
            await ctx.send("There was an error trying to reload this plugin: \n```\n{}\n```".format(ex))
        else:
            await ctx.send("Successfully reloaded ``{}``!".format(plugin))


def setup(bot): bot.add_cog(General(bot))
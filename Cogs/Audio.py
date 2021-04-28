import discord
from discord.ext import commands

import wavelink
from secrets import token_hex
from urllib.parse import urlparse



class Audio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, "wavelink"):
            self.bot.wavelink = wavelink.Client(bot=self.bot)
        
        self.bot.loop.create_task(self.start_nodes())
        self.states = {}

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        await self.bot.wavelink.initiate_node(
            host=self.bot.config['lavalink_host'],
            port=self.bot.config['lavalink_port'],
            rest_uri=f"http://{self.bot.config['lavalink_host']}:{self.bot.config['lavalink_port']}",
            password=self.bot.config['lavalink_password'],
            identifier=self.bot.config['lavalink_identifier'],
            region="frankfurt"
        )

    @commands.command(aliases=["join"])
    async def _connect(self, ctx, *, channel: discord.VoiceChannel = None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                return await ctx.send("You need to be in a voice channel in order to use this command")
        
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.connect(channel.id)


    @commands.command(aliases=["listen"])
    async def play(self, ctx, *, query):
        url = urlparse(query)
        query = "https://twitch.tv/" + url.path.strip("/")
        tracks = await self.bot.wavelink.get_tracks(query)
        if not tracks:
            return await ctx.send("This use is either doesn't exist or isn't streaming")
        
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self._connect)
        
        await player.set_volume(100)
        await player.play(tracks[0])
        self.states[ctx.guild.id] = tracks[0]
        await ctx.invoke(self.nowplaying)


    @commands.command(aliases=["stop", "dc", "disconnect"])
    async def leave(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.disconnect()
        self.states.pop(ctx.guild.id, None)
        try:
            await ctx.guild.voice_client.disconnect()
        except AttributeError:
            pass
        await ctx.send("Left the voice channel.")

    
    @commands.command(aliases=["np", "playing"])
    async def nowplaying(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            return await ctx.send("I'm currently not in a voice channel")
        
        state = self.states.get(ctx.guild.id)
        if state is None:
            return await ctx.send("I'm not playing anything right now")
        
        e = discord.Embed(
            color=self.bot.color,
            title="Now playing in {}".format(ctx.author.voice.channel.name),
            description=f"{state.title} \n{state.uri}"
        )
        e.set_footer(
            text="Type !!leave to stop the stream"
        )
        await ctx.send(embed=e)




def setup(bot):
    bot.add_cog(Audio(bot))
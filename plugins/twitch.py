import discord
from discord.ext import commands

import secrets
import random
import re



class Twitch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_regex = re.compile(f'^\w+$')
        self.badges = {
            "partner": "<:verified:836850404783292435>",
            "staff": "<:staff:836850404469374998>"
        }


    @commands.group()
    async def clips(self, ctx):
        if ctx.invoked_subcommand is None:
            e = discord.Embed(
                color=self.bot.color,
                title="Help - Clips",
                description="``clips game <game>`` - Clips tagged with a specific game \n``clips trending`` - Clips that are trending right now \n``clips user <user>`` -  Clips from a specific Twitch channel"
            )
            await ctx.send(embed=e)
    

    @clips.command()
    async def game(self, ctx, *, game):
        await ctx.trigger_typing()
        r = await self.bot.twitch_http.get("/search/games", {"query": game}, v5=True)
        if r.status > 399:
            return await ctx.send("Request returned with code {}".format(r.status))
        r = await r.json()
        if not r.get("games", False):
            return await ctx.send("No clips found")
        game = r["games"][0]["name"]
        r = await self.bot.twitch_http.get("/clips/top", {"limit": 50, "game": game}, v5=True)
        if r.status > 399:
            return await ctx.send("Request returned with code {}".format(r.status))
        r = await r.json()
        if not r.get("clips", False):
            return await ctx.send("No clips found")
        clip = random.choice(r["clips"])
        await ctx.send(f"{clip['url'].split('?')[0]}")


    @clips.command()
    async def user(self, ctx, user: str):
        await ctx.trigger_typing()
        user = user.split("/")[-1]
        if self.user_regex.match(user) is None:
            return await ctx.send("This doesn't look like a valid user")
        r = await self.bot.twitch_http.get("/clips/top", {"limit": 50, "channel": user}, v5=True)
        if r.status > 399:
            return await ctx.send("Request returned with code {}".format(r.status))
        r = await r.json()
        if not r.get("clips", False):
            return await ctx.send("No clips found")
        clip = random.choice(r["clips"])
        await ctx.send(f"{clip['url'].split('?')[0]}")


    @clips.command()
    async def trending(self, ctx):
        await ctx.trigger_typing()
        r = await self.bot.twitch_http.get("/clips/top", {"limit": 50}, v5=True)
        if r.status > 399:
            return await ctx.send("Request returned with code {}".format(r.status))
        r = await r.json()
        if not r.get("clips", False):
            return await ctx.send("No clips found")
        clip = random.choice(r["clips"])
        await ctx.send(f"{clip['url'].split('?')[0]}")


    @commands.command(name="user")
    async def _user(self, ctx, user: str):
        await ctx.trigger_typing()
        user = user.split("/")[-1]
        if self.user_regex.match(user) is None:
            return await ctx.send("This doesn't look like a valid user")
        
        r = await self.bot.twitch_http.get("/users", {"login": user})
        rj = (await r.json())
        if not rj.get("data", False) or r.status == 400:
            return await ctx.send("Twitch user not found")
        r.raise_for_status()
        rj = rj["data"][0]

        s = await self.bot.twitch_http.get("/streams", {"user_login": user})
        s.raise_for_status()
        s = (await s.json())["data"]

        ft = await self.bot.twitch_http.get("/users/follows", {"first": 1, "to_id": rj["id"]})
        ft.raise_for_status()

        ff = await self.bot.twitch_http.get("/users/follows", {"first": 1, "from_id": rj["id"]})
        ff.raise_for_status()

        emote = self.badges.get(rj["type"] or rj["broadcaster_type"], "")
        e = discord.Embed(
            color=self.bot.color,
            title=rj["login"] + " " + emote,
            description=rj["description"]
        )
        e.set_author(
            icon_url=rj["profile_image_url"],
            name=rj["display_name"],
            url=f"https://twitch.tv/{rj['login']}"
        )
        e.set_thumbnail(url=rj["profile_image_url"])
        e.add_field(
            name="Followers",
            value="{:,}".format((await ft.json())['total'])
        )
        e.add_field(
            name="Following",
            value="{:,}".format((await ff.json())['total'])
        )
        e.add_field(
            name="Views",
            value="{:,}".format(rj['view_count'])
        )

        if s:
            s = s[0]
            t = await self.bot.twitch_http.get("/streams/tags", {"broadcaster_id": rj["id"]})
            t.raise_for_status()
            tag_text = []
            for tag in (await t.json())["data"]:
                if not tag["is_auto"]:
                    tag_text.append(f"[{tag['localization_names']['en-us']}](https://twitch.tv/directory/all/tags/{tag['tag_id']})")
            if not tag_text:
                tag_text = ["No stream tags"]
            e.add_field(
                name="Stream Tags",
                value=", ".join(tag_text),
                inline=False
            )

            g = await self.bot.twitch_http.get("/games", {"id": s["game_id"]})
            g.raise_for_status()
            try:
                g = (await g.json())["data"][0]
            except Exception:
                g = {"name": "Unkown"}
            e.add_field(
                name="Currently Live",
                value=f"**{s['title']}**\n"
                + "Playing {} for {} viewers".format(g['name'], s['viewer_count'])
                + f"\n\n**[Watch on Twitch](https://twitch.tv/{user})**"
            )
            e.set_image(
                url=s["thumbnail_url"].format(width=1920, height=1080) + f"?{secrets.token_urlsafe(5)}"
            )
        await ctx.send(embed=e)


def setup(bot): bot.add_cog(Twitch(bot))
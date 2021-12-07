import discord



class Embed(discord.Embed):
    def __init__(self, *args, color=0x9146ff, **kwargs):
        super().__init__(*args, color=color, **kwargs)

    def add_field(self, name, value, inline=False):
        super().add_field(name, value, inline)


async def get_notifs(bot, guild_id) -> list:
    if not guild_id in bot.notif_cache:
        for doc in bot.db.notifications.find({"id": f"{guild_id}"}):
            n = doc["notifications"]; bot.notif_cache[guild_id] = n
            if n is None:
                return []
            else:
                return n
    else:
        return bot.notif_cache[guild_id]


async def is_live(bot, streamer) -> bool:
    r = await bot.twitch_http.get("/streams", {"user_login": streamer})
    r = (await r.json())["data"]
    if r:
        r = r[0]
        return True, r
    else:
        return False, {}

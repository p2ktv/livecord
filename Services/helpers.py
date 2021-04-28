async def get_notifs(bot, guild_id) -> list:
    for doc in bot.db.notifications.find({"id": f"{guild_id}"}):
        n = doc["notifications"]
        if n is None:
            return []
        else:
            return n


async def is_live(bot, streamer) -> bool:
    r = await bot.twitch_http.get("/streams", {"user_login": streamer})
    r = (await r.json())["data"]
    if r:
        r = r[0]
        return True, r
    else:
        return False, {}

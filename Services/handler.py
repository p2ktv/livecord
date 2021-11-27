import discord

import asyncio
import secrets
import traceback

from Services import helpers



async def handle_notifications(bot):
    while True:
        await asyncio.sleep(60)

        for g in bot.guilds:

            notifs = await helpers.get_notifs(bot, g.id)
            if len(notifs) > 0:
                for entry in notifs:

                    status, s_data = await helpers.is_live(bot, entry['user'])
                    if status is True:

                        if not entry['user'] in bot.sent_notifications:
                            
                            # get user data
                            u_data = await bot.twitch_http.get("/users", {"login": entry['user']})
                            u_data = (await u_data.json())
                            u_data = u_data["data"][0]

                            # get game data
                            g_data = await bot.twitch_http.get("/games", {"id": s_data["game_id"]})
                            try:
                                g_data = (await g_data.json())["data"][0]
                            except Exception:
                                g_data = {"name": "Unkown"}

                            # define embed
                            e = discord.Embed(
                                color=bot.color,
                                description="**[{}](https://twitch.tv/{})**".format(s_data['title'], entry['user'])
                            )
                            e.set_author(name="{}".format(entry['user']), icon_url=u_data["profile_image_url"])
                            e.set_thumbnail(
                                url=u_data["profile_image_url"]
                            )
                            e.add_field(
                                name="Game/Category",
                                value=g_data['name'],
                                inline=True
                            )
                            e.add_field(
                                name="Viewers",
                                value="{:,}".format(s_data['viewer_count'])
                            )
                            e.set_image(
                                url=s_data["thumbnail_url"].format(width=1920, height=1080) + f"?{secrets.token_urlsafe(5)}"
                            )
                            try:
                                channel = await bot.fetch_channel(int(entry['channel']))
                                await channel.send(content=entry['message'], embed=e)
                            finally:
                                bot.sent_notifications.append(entry['user'])
                    else:
                        if entry['user'] in bot.sent_notifications:
                            bot.sent_notifications.remove(entry['user'])







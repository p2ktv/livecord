import requests as r
import discord

from Cogs.API import API
from Cogs import Config



noti_channel = None
BOT = None


async def init(bot):
    global noti_channel
    global BOT
    noti_channel = await bot.fetch_channel(int(Config.CHANNEL))
    BOT = bot



async def get_twitch_data(channel_name):
    # check if the token is still usable
    api_token = BOT.api_cache["access_token"]

    headers = {
        "client-id": f"{Config.CLIENT_ID}",
        "Authorization": f"Bearer {api_token}"
    }


    channel_url = "https://api.twitch.tv/helix/search/channels?query={}".format(channel_name)
    channel_data = None
    for x in r.get(url=channel_url, headers=headers).json()["data"]:
        if x["display_name"].lower() != channel_name.lower():
            pass
        else:
            channel_data = x

    if channel_data["is_live"] is False:
        return None, None, None # return none if the channel isn't live

    channel_id = channel_data["id"]

    stream_url = "https://api.twitch.tv/helix/streams?user_id={}".format(channel_id)
    stream_data = None
    for y in r.get(url=stream_url, headers=headers).json()["data"]:
        if y["user_id"] != str(channel_id):
            pass
        else:
            stream_data = y

    user_icon_url = "https://api.twitch.tv/helix/users?id={}".format(channel_id)
    icon_url = None
    for z in r.get(url=user_icon_url, headers=headers).json()["data"]:
        if z["id"] != str(channel_id):
            pass
        else:
            icon_url = z["profile_image_url"]

    return channel_data, stream_data, icon_url
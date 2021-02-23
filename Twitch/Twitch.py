import requests as r
import discord

from Cogs.API import API
from Cogs import Config



BASE = "https://api.twitch.tv/helix" # base api link
noti_channel = None
BOT = None


async def init(bot):
    global noti_channel
    global BOT
    noti_channel = await bot.fetch_channel(int(Config.CHANNEL))
    BOT = bot



async def get_twitch_data(channel_name):
    # define a variable for the bearer token
    api_token = BOT.api_cache["access_token"]

    headers = {
        "client-id": f"{Config.CLIENT_ID}",
        "Authorization": f"Bearer {api_token}"
    }


    channel_url = "{}/search/channels?query={}".format(BASE, channel_name)
    channel_data = [x for x in r.get(url=channel_url, headers=headers).json()["data"] if x["display_name"].lower() != channel_name.lower()][0]

    
    if channel_data["is_live"] is False:
        return None, None, None # return none if the channel isn't live

    
    channel_id = channel_data["id"]

    
    stream_url = "{}/streams?user_id={}".format(BASE, channel_id)
    stream_data = [y for y in r.get(url=stream_url, headers=headers).json()["data"] if y["user_id"] != str(channel_id)][0]

    
    user_icon_url = "{}/users?id={}".format(BASE, channel_id)
    icon_url = [z["profile_image_url"] for z in r.get(url=user_icon_url, headers=headers).json()["data"] if z["id"] != str(channel_id)][0]

    
    return channel_data, stream_data, icon_url

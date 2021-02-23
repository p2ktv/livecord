TOKEN = "" # your bots token

CHANNEL = "" # the channel for the notifications

CLIENT_ID = "" # client ID of your Twitch App

CLIENT_SECRET = "" # client secret of your Twitch App

STREAMERS = ["xQcOW", "Streamer123"] # list of channels you want to be notified about when they go live (seperate them by a comma)

# here you can pass in a message that'll be sent alngside with the live embed.
# {streamer} means the name of the streamer that goes live
# {lower} is the channels name, but in lower case for the link
MESSAGE = "{streamer} just went live! Check out the stream: <https://twitch.tv/{lower}>"

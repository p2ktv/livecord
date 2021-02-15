# Twitch-Bot

### How do I run it?

This isn' a bot you can add via a link. If you want to use it, you have to host your own instance. Here's a quick guide on how to do so:

1: **Install Python 3.5+**

You need the Python version in order to actually run an instance of the bot

2: **Install the dependencies**

Do so by running `pip install -U -r requirements.txt` in your terminal

3: **Setup the config file**

Go into the `Cogs` directory na dopen the `Config.py` file. There you need to pass in the requested tokens/secrets.
The file should look something like this:

```py
TOKEN = "" # your bots token

CHANNEL = "" # the channel for the notifications

CLIENT_ID = "" # client ID of your Twitch App

CLIENT_SECRET = "" # client secret of your Twitch App

STREAMERS = ["xQcOW"] # list of channels you want to be notified about when they go live (seperate them by a comma)

# here you can pass in a message that'll be sent alongside with the live embed.
# {streamer} means the name of the streamer that goes live
# {lower} is the channels name, but in lower case for the link
MESSAGE = "{streamer} just went live! Check out the stream: <https://twitch.tv/{lower}>"
```

5: **Run the bot**

Now run the bot by typing `py -3 Main.py` into your terminal

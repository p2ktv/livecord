# Notification-Bot

### How do I run it?

This isn't a public bot. If you want to use it, you have to host your own instance. Here's a quick guide on how to do so:

1: **Install Python 3.5+**

You need this Python version in order to actually run an instance of the bot

2: **Install the dependencies**

Do so by running `pip install -U -r requirements.txt` in your terminal

3: **Get your Twitch Secrets**

Visit [this site](https://dev.twitch.tv/console/apps) and click the "Register Your Application" button in the top left corner. Once clicked, you pass in a name (doesn't really matter what) and a redirect URL. You might not know what exactly that is, but for this simple bot it's enough if you pass `http://localhost:3000` into that field. Then choose a category (doesn't really matter either), solve the captcha, and hit "Create".
Next thing is to click the "Manage" button of your new app in order to see the `Client ID` and the `Client Secret` (you might have to click "New Secret" to view it) for the next step.

4: **Set up the config file**

Go into the `Cogs` directory and open the `Config.py` file. There you need to pass in the requested tokens/secrets.
The file should look something like this:

```py
TOKEN = "" # your bots token

CHANNEL = "" # the channel for the notifications

CLIENT_ID = "" # client ID of your Twitch App

CLIENT_SECRET = "" # client secret of your Twitch App

STREAMERS = ["xQcOW", "Streamer123"] # list of channels you want to be notified about when they go live (separate them by a comma)

# here you can pass in a message that'll be sent alongside the live embed.
# {streamer} means the name of the streamer that goes live
# {lower} is the channels name, but in lower case for the link
MESSAGE = "{streamer} just went live! Check out the stream: <https://twitch.tv/{lower}>"
```

5: **Run the bot**

Now run the bot by typing `py -3 Main.py` into your terminal

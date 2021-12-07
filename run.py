from discord import Intents
from discord.ext import commands

import json
import logging

from core import Livecord



def log_setup():
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s @ %(name)s [%(asctime)s] - %(message)s",
        datefmt="%d-%b %H:%M:%S"
    )
    logging.captureWarnings(True)
    log = logging.getLogger("livecord")


if __name__ == "__main__":
    log_setup()

    with open("./config.json", "r") as f:
        config = json.load(f)
    bot = Livecord(config=config)

    try:
        bot.run()
    except KeyboardInterrupt:
        bot.loop.run_until_complete(bot.logout())

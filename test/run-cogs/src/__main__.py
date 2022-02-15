import os
import platform
from multiprocessing import Process
import threading

import nextcord
from alive_progress import alive_bar
from nextcord.ext import commands

from cogs.etc.config import TOKEN, PREFIX, PROJECT_NAME, AUTHORID
from cogs.etc.config import OAUTH, BOT_USERNAME, tPREFIX, CHANNEL_NAME

from define_global_vars import define_global_vars

from twitchio.ext import commands as tcommands


intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX,
                   intents=intents,
                   help_command=None,
                   description=f"Created by exersalza. Project: {PROJECT_NAME}")

tbot = tcommands.Bot(
    token=OAUTH,
    nick=BOT_USERNAME,
    prefix=tPREFIX,
    initial_channels=CHANNEL_NAME)

# tbot.load_module('cogs.twitchXdiscord')


count = 0
names = ['__init__.py', 'playground.py', 'gtarp_stuff.py', 'test.py']

for f in os.listdir('cogs'):
    if f.endswith(".py") and f not in names:
        count += 1


def load():
    with alive_bar(count) as bar:
        for filename in os.listdir("cogs"):
            if filename.endswith(
                    ".py"
            ) and filename not in names:
                loader = f"cogs.{filename[:-3]}"
                tbot.load_module(loader)
                bar()


if __name__ == '__main__':
    platform = platform.system()

    command = 'cls'

    if platform == 'Linux':
        command = 'clear'

    os.system(command)

    load()
    bot = define_global_vars(bot)

    discord = threading.Thread(target=bot.run(bot.token), daemon=True)
    twitch = Process(target=tbot.run())

    twitch.start()
    # discord.run()
    # Client = Process(target=bot.run(bot.token))
    # Client.start()

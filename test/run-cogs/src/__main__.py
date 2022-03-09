import os
import platform
import pprint
from multiprocessing import Process

import nextcord
from alive_progress import alive_bar
from nextcord.ext import commands

from cogs.etc.config import PREFIX, PROJECT_NAME, SHARDS
from define_global_vars import define_global_vars

# from cogs.etc.config import OAUTH, BOT_USERNAME, tPREFIX, CHANNEL_NAME

intents = nextcord.Intents.all()
bot = commands.AutoShardedBot(command_prefix=PREFIX,
                              shard_count=SHARDS,
                              intents=intents,
                              help_command=None,
                              description=f"Created by exersalza. Project: {PROJECT_NAME}")


# tbot = tcommands.Bot(
#     token=OAUTH,
#     nick=BOT_USERNAME,
#     prefix=tPREFIX,
#     initial_channels=CHANNEL_NAME)

# tbot.load_module('cogs.twitchXdiscord')


count = 0
names = ['__init__.py', '__pycache__', 'playground.py', 'gtarp_stuff.py', 'twitchXdiscord.py']
excluded_dirs = ['__pycache__', 'etc', 'logs']

for f in os.listdir('cogs'):
    if f.endswith(".py") and f not in names:
        count += 1


def load():
    with alive_bar(count) as bar:
        for dirname in os.listdir("cogs"):
            if dirname not in excluded_dirs + names:
                for filename in os.listdir(f'cogs/{dirname}'):
                    if filename not in names:
                        loader = f"cogs.{dirname}.{filename[:-3]}"
                        print(loader)
                        bot.load_extension(loader)
                        bar()


if __name__ == '__main__':
    platform = platform.system()

    command = 'cls'

    if platform == 'Linux':
        command = 'clear'

    # subprocess.call([command], shell=False)

    load()
    bot = define_global_vars(bot)

    discord = Process(target=bot.run(bot.token))
    # twitch = Process(target=tbot.run())

    discord.start()
    # discord.run()
    # Client = Process(target=bot.run(bot.token))
    # Client.start()

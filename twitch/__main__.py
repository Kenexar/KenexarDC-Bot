import os
import platform
from multiprocessing import Process

from alive_progress import alive_bar
from twitchio.ext import commands

from cogs.etc import config

# event_usernotice_subscription(payload)


bot = commands.Bot(token=config.OAUTH,
                   nick=config.BOT_USERNAME,
                   prefix=config.PREFIX,
                   initial_channels=config.CHANNEL_NAME)

names = ['__init__.py']
count = 0

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
                bot.load_module(loader)
                bar()


if __name__ == '__main__':
    platform = platform.system()

    command = 'cls'

    if platform == 'Linux':
        command = 'clear'

    os.system(command)

    load()

    Client = Process(target=bot.run())
    Client.start()

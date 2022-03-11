import os
import platform
import subprocess
import time
from multiprocessing import Process

import nextcord
from alive_progress import alive_bar
from nextcord.ext import commands

from cogs.etc.config import PREFIX, PROJECT_NAME, SHARDS
from cogs.etc.flask_server import start_server
from define_global_vars import define_global_vars

intents = nextcord.Intents.all()
bot = commands.AutoShardedBot(command_prefix=PREFIX,
                              shards=SHARDS,
                              intents=intents,
                              help_command=None,
                              description=f"Created by exersalza. Project: {PROJECT_NAME}",)

count = 0
names = ['__init__.py', '__pycache__', 'playground.py', 'gtarp_stuff.py']
excluded_dirs = ['__pycache__', 'etc', 'logs', 'logger']

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
    try:
        subprocess.call([command], shell=False, timeout=1)
    except FileNotFoundError:
        pass

    print("""
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│     ██╗  ██╗███████╗███╗   ██╗███████╗██╗  ██╗ █████╗ ██████╗      │
│     ██║ ██╔╝██╔════╝████╗  ██║██╔════╝╚██╗██╔╝██╔══██╗██╔══██╗     │
│     █████╔╝ █████╗  ██╔██╗ ██║█████╗   ╚███╔╝ ███████║██████╔╝     │
│     ██╔═██╗ ██╔══╝  ██║╚██╗██║██╔══╝   ██╔██╗ ██╔══██║██╔══██╗     │
│     ██║  ██╗███████╗██║ ╚████║███████╗██╔╝ ██╗██║  ██║██║  ██║     │
│     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝     │
│                                                                    │
└────────────────────────┤ ZerXDE & exersalza├───────────────────────┘\n""")

    bot = define_global_vars(bot)

    load()
    if bot.flask:
        print('\u001b[32m/----------[ FLASK ]----------\\\u001b[0m'.center(80))
        start_server()
        time.sleep(.5)

        print('\u001b[32m\\----------[ FLASK ]----------/\u001b[0m'.center(80))

    Client = Process(target=bot.run(bot.token))
    Client.start()

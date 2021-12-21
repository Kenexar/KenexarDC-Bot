import os
import platform
import time
from multiprocessing import Process

import nextcord
from alive_progress import alive_bar
from nextcord.ext import commands
from pyfiglet import Figlet

from cogs.etc.config import TOKEN, PREFIX, FLASK, PROJECT_NAME
from cogs.etc.flask_server import start_server
# ja
intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX,
                   intents=intents,
                   help_command=None,
                   description=f"Created by exersalza. Project: {PROJECT_NAME}")

count = 0
names = ['__init__.py', 'playground.py', 'embeds.py']

for f in os.listdir('cogs'):
    if f.endswith(".py") and not f in names:
        count += 1


def load():
    with alive_bar(count) as bar:
        for filename in os.listdir("cogs"):
            if filename.endswith(
                    ".py"
            ) and filename not in names:
                loader = f"cogs.{filename[:-3]}"
                bot.load_extension(loader)
                bar()


if __name__ == '__main__':
    platform = platform.system()

    if platform == 'Windows':
        clear = lambda: os.system('cls')
        clear()
    elif platform == 'Linux':
        clear = lambda: os.system('clear')
        clear()

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

    load()
    if FLASK:
        print('\u001b[32m/----------[ FLASK ]----------\\\u001b[0m'.center(80))
        start_server()
        time.sleep(.5)

        print('\u001b[32m\\----------[ FLASK ]----------/\u001b[0m'.center(80))

    Client = Process(target=bot.run(TOKEN))
    Client.start()

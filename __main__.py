import os
import platform
from multiprocessing import Process
import time

import nextcord
from alive_progress import alive_bar
from nextcord.ext import commands
from pyfiglet import Figlet

from cogs.etc.config import TOKEN, PREFIX, FLASK
from cogs.etc.server import start_server

intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX,
                   intents=intents,
                   help_command=None,
                   description="Created by exersalza. Project: SunSide")

count = 0

for f in os.listdir('cogs'):
    if f.endswith(".py") and f != "__init__.py" and f != "playground.py":
        count += 1


def load():
    with alive_bar(count) as bar:
        for filename in os.listdir("cogs"):
            if filename.endswith(
                    ".py"
            ) and filename != "__init__.py" and filename != "playground.py":
                bot.load_extension(f"cogs.{filename[:-3]}")
                bar()


if __name__ == '__main__':
    platform = platform.system()

    if platform == 'Windows':
        clear = lambda: os.system('cls')
        clear()
    elif platform == 'Linux':
        clear = lambda: os.system('clear')
        clear()

    print(f'\u001b[36m{Figlet(font="chunky").renderText("Kenexar")}\u001b[0m')
    load()
    if FLASK:
        print('\u001b[32m/----------[ FLASK ]----------\\\u001b[0m'.center(80))
        start_server()
    time.sleep(.5)
    if FLASK:
        print('\u001b[32m\\----------[ FLASK ]----------/\u001b[0m'.center(80))

    Client = Process(target=bot.run(TOKEN))
    Client.start()

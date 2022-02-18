import json
from datetime import datetime

import nextcord
import requests
from nextcord.ext import commands
from nextcord.ext import tasks


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Test(bot))

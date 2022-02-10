import nextcord
from nextcord.ext import commands
import os, sys


class Neofetch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Command
    async def neofetch(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Neofetch(bot))

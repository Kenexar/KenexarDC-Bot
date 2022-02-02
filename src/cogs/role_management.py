from nextcord.ext import commands
from cogs.etc.config import dbBase


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Command
    async def createrole(self, ctx):
        cur = dbBase.cursor()
        pass


def setup(bot):
    bot.add_cog(Roles(bot))

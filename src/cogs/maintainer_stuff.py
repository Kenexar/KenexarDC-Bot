import os

from cogs.etc.config import AUTHORID
from nextcord.ext import commands


class MaintainerStuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Command
    async def restart(self, ctx):
        if not ctx.author.id == AUTHORID:
            return

        await ctx.send('Starting doomsday protocol, please wait...')
        os.system('./restart.sh')


def setup(bot):
    bot.add_cog(MaintainerStuff(bot))

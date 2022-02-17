import os
import subprocess

from nextcord.ext import commands
from nextcord.ext.commands import CommandNotFound


class MaintainerStuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Command
    async def restart(self, ctx):
        """ Owner Bot restart command. Thre bot has also an Module reload module, but its not here

        :param ctx:
        :type ctx:
        :return:
        :rtype:
        """
        if not ctx.author.id == self.bot.authorid:
            raise CommandNotFound

        await ctx.send('Starting doomsday protocol, please wait...')
        subprocess.call('./restart.sh', shell=False)


def setup(bot):
    bot.add_cog(MaintainerStuff(bot))

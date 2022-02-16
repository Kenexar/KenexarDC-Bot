import os

from nextcord.ext import commands


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
            return

        await ctx.send('Starting doomsday protocol, please wait...')
        os.system('./restart.sh')


def setup(bot):
    bot.add_cog(MaintainerStuff(bot))

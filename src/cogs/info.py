import nextcord
from nextcord.ext import commands


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Command
    async def info(self, ctx):
        message = """ Bot Author exersalza#1337
**Github:** https://github.com/kenexar
**Github: (me)** https://github.com/exersalza

**Website:** https://kenexar.eu        
        """
        await ctx.send(message)


def setup(bot):
    bot.add_cog(Info(bot))

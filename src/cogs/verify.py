from nextcord.ext import commands


class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Command
    async def setchannel(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Verify(bot))

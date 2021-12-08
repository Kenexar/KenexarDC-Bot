from nextcord.ext import commands


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Command
    async def info(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Info(bot))

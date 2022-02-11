from nextcord.ext import commands


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(self.bot.authorid)


def setup(bot):
    bot.add_cog(Test(bot))

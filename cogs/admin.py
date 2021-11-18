from nextcord.ext import commands

#todo:
#   get, del, add, clear


class Admin(commands.cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def get(self, ctx, *args):
        pass

    @commands.command()
    async def delete(self, ctx):
        pass

    @commands.command()
    async def add(self, ctx):
        pass

    @commands.command()
    async def clear(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Admin(bot))

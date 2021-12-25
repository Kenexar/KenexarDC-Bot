from cogs.etc.config import dbBase
from cogs.etc.config import PROJECT_NAME

from discord.ext import commands


class Points(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def top(self, ctx):
        # Top placed on the Server
        cursor = dbBase.cursor()

        cursor.execute("SELECT User, Points FROM points WHERE Name=%s", (PROJECT_NAME,))

        fetcher = cursor.fetchall()

        for i in fetcher:
            print(i)

        cursor.close()
        pass

    @commands.command()
    async def pinfo(self, ctx, user=None):
        # Show the Player information for the Game lulw, it returns an embed i think
        cursor = dbBase.cursor()



        cursor.close()
        pass


def setup(bot):
    bot.add_cog(Points(bot))

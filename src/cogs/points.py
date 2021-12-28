from cogs.etc.config import dbBase
from cogs.etc.config import PROJECT_NAME
from cogs.etc.presets import lvl_up, add_points

from discord.ext import commands


class Points(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        cur = dbBase.cursor()

        cur.execute("SELECT Level, Points FROM points WHERE User=%s;", (message.author.id,))
        fetcher = cur.fetchone()

        if not fetcher:
            cur.execute("INSERT INTO points(User, Points, Level, Name) VALUES (%s, %s, %s, %s);", (message.author.id, 0, 1, PROJECT_NAME))
            dbBase.commit()
            cur.close()
            return

        add_points(message.author.id, cur, fetcher)

        if lvl_up(message.author.id, cur, fetcher):
            await message.channel.send(f'{message.author.mention} Just leveld up to {fetcher[0]}, yippie')


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

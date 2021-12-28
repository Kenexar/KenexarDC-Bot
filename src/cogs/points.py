from datetime import datetime

import nextcord
from src.cogs.etc.config import dbBase
from src.cogs.etc.config import PROJECT_NAME
from src.cogs.etc.presets import lvl_up, add_points

from discord.ext import commands

from src.cogs.etc.config import EMBED_ST


class Points(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        cur = dbBase.cursor()

        cur.execute("SELECT Level, Points, Multiplier FROM points WHERE User=%s;", (message.author.id,))
        fetcher = cur.fetchone()

        if not fetcher:
            cur.execute("INSERT INTO points(User, Points, Level, Multiplier, Name) VALUES (%s, %s, %s, %s, %s);",
                        (message.author.id, 0, 1, 1, PROJECT_NAME))
            dbBase.commit()
            cur.close()
            return

        add_points(message.author.id, cur, fetcher)

        if lvl_up(message.author.id, cur, fetcher):
            await message.channel.send(f'{message.author.mention} Just leveld up to {int(fetcher[0]) + 1}, yippie')

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
    async def level(self, ctx, user=None):
        # Show the Player information for the Game lulw, it returns an embed i think
        cur = dbBase.cursor()

        cur.execute("SELECT Level, Points, Multiplier FROM points WHERE User=%s;",
                    (user.strip("<@!>") if user else ctx.message.author.id,))

        fetcher = cur.fetchone()

        level = fetcher[0]
        exp = fetcher[1]
        multi = fetcher[2]

        username = await self.bot.fetch_user(user.strip("<@!>")) if user else ctx.message.author.name

        embed = nextcord.Embed(title=f'Level info for {username}',
                               description=f'Current Level: {level}\n'
                                           f'Current Points: {exp}\n'
                                           f'Current Multiplier: {multi}x',
                               color=EMBED_ST,
                               timestamp=datetime.now())

        await ctx.send(embed=embed)
        cur.close()
        pass


def setup(bot):
    bot.add_cog(Points(bot))

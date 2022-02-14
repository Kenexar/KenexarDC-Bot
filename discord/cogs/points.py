from datetime import datetime

import nextcord
from cogs.etc.presets import lvl_up, add_points
from discord.ext import commands


# Todo:
# server deactivate/activate

class Points(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        cur = self.bot.dbBase.cursor(buffered=True)

        cur.execute("SELECT Level, Experience, Multiplier, Coins FROM points WHERE User=%s;", (message.author.id,))
        fetcher = cur.fetchone()

        if not fetcher:
            cur.execute(
                "INSERT INTO points(User, Coins, Experience, Level, Multiplier, Name) VALUES (%s, %s, %s, %s, %s, %s);",
                (message.author.id, 100, 0, 1, 1, self.bot.project_name))
            self.bot.dbBase.commit()
            cur.close()
            return

        await add_points(message.author.id, cur, fetcher)

        if await lvl_up(message.author.id, cur, fetcher):
            await message.channel.send(f'{message.author.mention} Just leveld up to {int(fetcher[0]) + 1}, yippie')
        cur.close()

    @commands.command()
    async def top(self, ctx):
        # Top placed on the Server
        cursor = self.bot.dbBase.cursor(buffered=True)

        cursor.execute("SELECT User, Points FROM points WHERE Name=%s", (self.bot.project_name,))

        fetcher = cursor.fetchall()

        for i in fetcher:
            print(i)

        cursor.close()
        pass

    @commands.command()
    async def level(self, ctx, user=None):
        # Show the Player information for the Game lulw, it returns an embed i think
        cur = self.bot.dbBase.cursor()

        cur.execute("SELECT Level, Experience, Multiplier, Coins FROM points WHERE User=%s and Name=%s;",
                    (user.strip("<@!>") if user else ctx.message.author.id, self.bot.project_name))

        fetcher = cur.fetchone()

        if not fetcher:
            return await ctx.send(
                f'{ctx.message.author.mention if not user else user} has not send an Message to the Server!')

        level = fetcher[0]
        exp = fetcher[1]
        multi = fetcher[2]
        coins = fetcher[3]

        username = await self.bot.fetch_user(user.strip("<@!>")) if user else ctx.message.author.name

        embed = nextcord.Embed(title=f'Level info for {username}',
                               description=f'Current Level: {level}\n'
                                           f'Current Experience: {exp}\n'
                                           f'Current Multiplier: {multi}x\n'
                                           f'Current Coins: {coins}',
                               color=self.bot.embed_st,
                               timestamp=self.bot.current_timestamp)

        await ctx.send(embed=embed)
        cur.close()

    @commands.Command
    async def enablepoints(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Points(bot))
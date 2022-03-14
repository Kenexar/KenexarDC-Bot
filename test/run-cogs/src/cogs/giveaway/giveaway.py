import datetime

import nextcord
from nextcord.ext import commands


class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Command
    async def giveaway(self, ctx: commands.Context):
        message = ctx.message

        if len(message.content.split()) == 1:
            embed = nextcord.Embed(title='Create a Giveaway help',
                                   color=self.bot.embed_st,
                                   timestamp=self.bot.current_timestamp())
            embed.add_field(name='Giveaway',
                            value='`$giveaway (Title) ~(Days)` -> Type a title for the Giveaway, Days: type behind the `~` the number of days the Giveaway should go and its optional, the default is 2 days',
                            inline=False)

            await ctx.send(embed=embed)
            return

        content = message.content.split('~')
        title = content[0][10:]
        days = content[1].strip()

        if not days.isdigit():
            return await ctx.send('Days parameter is not a number', delete_after=20)

        embed = nextcord.Embed(title=title,
                               description='User entered Giveaway: `0`',
                               color=self.bot.embed_st,
                               timestamp=datetime.datetime.now() + datetime.timedelta(days=int(days)))

        embed.set_footer(text='Deadline ')
        m = await ctx.send(embed=embed)


class GiveawayBackend(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Giveaway(bot))
    bot.add_cog(GiveawayBackend(bot))

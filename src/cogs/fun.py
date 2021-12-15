from nextcord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Command
    async def opfer(self, ctx):
        await ctx.send(f'Maul {ctx.message.author.mention}')


def setup(bot):
    bot.add_cog(Fun(bot))

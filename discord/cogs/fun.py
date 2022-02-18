from nextcord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Command
    async def opfer(self, ctx):
        await ctx.send(f'Maul {ctx.message.author.mention}')

    @commands.Command  # testing some stuff
    async def bug(self, ctx):
        return await ctx.send(f'There are no Bugs! only features!')


def setup(bot):
    bot.add_cog(Fun(bot))

from nextcord.ext import commands


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Command
    async def setjtc(self, ctx):
        arg = ctx.message.content.split()
        print(arg)
        if len(arg) != 2:
            return await ctx.send('No valid argument range')

def setup(bot):
    bot.add_cog(Test(bot))

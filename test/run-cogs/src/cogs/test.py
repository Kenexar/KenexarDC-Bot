import nextcord
from nextcord.ext import commands
from nextcord.ui import View


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Command
    async def get_avatar(self, ctx: commands.Context, member: nextcord.Member):
        print(member.avatar.url)


def setup(bot):
    bot.add_cog(Test(bot))

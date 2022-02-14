from nextcord.ext import commands


class MemberManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_joined(self, member):
        print(member)


def setup(bot):
    bot.add_cog(MemberManager(bot))

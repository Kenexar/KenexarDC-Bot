from nextcord.ext import commands


class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Giveaway(bot))

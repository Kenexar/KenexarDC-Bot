from nextcord.ext import commands
from nextcord.ext.commands import has_permissions
from cogs.etc.presets import fillup


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Test(bot))

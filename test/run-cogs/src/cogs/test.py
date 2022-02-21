import nextcord
from nextcord import ButtonStyle
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions
from nextcord.ui import Button, Item
from nextcord.ui import View


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('ready, pls dont delete me :(')


def setup(bot):
    bot.add_cog(Test(bot))

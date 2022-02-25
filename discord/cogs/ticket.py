from nextcord.ext import commands
from nextcord.ext.commands import has_permissions


class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Command
    @has_permissions(administrator=True)
    async def settickets(self, ctx, ticket_channel_id):
        pass




def setup(bot):
    bot.add_cog(Ticket(bot))

import nextcord
from nextcord.ext import commands

from cogs.etc.config import dbBase


class AutoResponse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        print(int(message.guild.id))
        return
        cur = dbBase.cursor()

        cur.execute('select channel_id from serverchannel where server_id = %s', (int(message.guild.id),))
        channel = cur.fetchone()[0]
        if message.channel.id == channel:
            await message.add_reaction("<:check:926545063641747506>")
            await message.add_reaction("<:block:926545051172077579>")


def setup(bot):
    bot.add_cog(AutoResponse(bot))

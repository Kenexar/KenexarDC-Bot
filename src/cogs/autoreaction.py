import nextcord
from nextcord.ext import commands

from cogs.etc.config import dbBase


class AutoResponse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        cur = dbBase.cursor(buffered=True)

        cur.execute('select channel_id from serverchannel where server_id=%s', (int(message.guild.id),))
        fetcher = cur.fetchone()
        cur.close()

        if not fetcher:
            cur.close()
            return
        channel = fetcher[0]

        # if message.channel.id == channel:
        #     await message.add_reaction("👍")
        #     await message.add_reaction("👎")


def setup(bot):
    bot.add_cog(AutoResponse(bot))

from twitchio.ext import commands


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.event()
    async def event_message(self, message):
        print(message)
        if message.echo:
            return

        print(message.content)


def prepare(bot):
    bot.add_cog(Welcome(bot))

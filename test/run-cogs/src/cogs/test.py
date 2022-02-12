from nextcord.ext import commands


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.ch = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.ch = self.bot.get_channel(801843320543641652)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 942082659885146133:
            if 'MessageType.premium_guild' in str(message.type):
                await self.ch.send(f'{message.author.name} hat den Server geboosted, Danke :)')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.ch.send(f'{member.name} ist dem Server beigetreten. Willkommen im Rift')


def setup(bot):
    bot.add_cog(Test(bot))

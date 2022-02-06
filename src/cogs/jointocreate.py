import nextcord
from nextcord.ext import commands

from cogs.etc.presets import fillup


class JoinToCreate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.jointocreate_channel = fillup

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # Todo: remove channel when no ones is inside of it
        #
        # You delete a channel from the user category and don't delete the main channel
        try:
            if after.channel.id == 939593836798296094:
                guild = self.bot.get_guild(member.guild.id)
                category = self.bot.get_channel(939595007327883274)

                channel = await guild.create_voice_channel(name=f'{member.name}\'s Voice',
                                                           category=category)

                await channel.edit(sync_permissions=True)
                await member.move_to(channel=channel)

        except AttributeError:
            pass


def setup(bot):
    bot.add_cog(JoinToCreate(bot))

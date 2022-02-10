import nextcord
from nextcord.ext import commands

from cogs.etc.presets import fillup


class JoinToCreate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.jtc_channel: dict = fillup(5)
        self.jtc_category: dict = fillup(6)

        self.jtc_current_channel = []

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # Todo: remove channel when no ones is inside of it
        #
        # You delete a channel from the user category and don't delete the main channel
        guild_has_jtc = self.jtc_channel.get(member.guild.id)

        if guild_has_jtc:
            try:
                if after.channel.id in guild_has_jtc:
                    guild = self.bot.get_guild(member.guild.id)
                    category = self.bot.get_channel(self.jtc_category[member.guild.id][0])

                    channel = await guild.create_voice_channel(name=f'{member.name}\'s Voice',
                                                               category=category)

                    self.jtc_current_channel.append(channel.id)
                    await self.channel_creator(channel, member)
            except AttributeError:
                pass
        try:
            if before.channel.id in self.jtc_current_channel and guild_has_jtc:
                channel = self.bot.get_channel(before.channel.id)

                if not await self.count_member_in_voice(channel):
                    await channel.delete()
        except AttributeError:
            pass

    async def count_member_in_voice(self, channel):
        user_in_voice = []
        for member in channel.members:
            user_in_voice.append(member.id)
        return user_in_voice

    async def channel_creator(self, channel, member):
        await channel.edit(sync_permissions=True)
        await member.move_to(channel=channel)


def setup(bot):
    bot.add_cog(JoinToCreate(bot))

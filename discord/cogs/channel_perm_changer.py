import nextcord
from nextcord.ext import commands


# todo:
# Changeable channel sizes
# Channel Name
# Channel Current owner, Change owner, Claim owner
# Channel Info
#


class ChannelPermChanger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.changeable_perm_list = [
            'size',
            'owner',
            'claim-owner',
            'set-owner',
            'name',
            'info'
        ]

    # @commands.command(name='channel')
    @nextcord.slash_command(name='channel', description='Change settings in your Private voice channel', guild_ids=[],
                            force_global=True)
    async def _channel(self, interaction: nextcord.Interaction):
        # Maybe subcommands?
        return await interaction.response.send_message('...Maintenance...')


def setup(bot):
    bot.add_cog(ChannelPermChanger(bot))

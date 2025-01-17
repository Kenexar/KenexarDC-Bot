import nextcord
from nextcord.ext import commands


async def send_interaction_msg(message: str, interaction: nextcord.Interaction, tmp=True):
    try:
        await interaction.followup.send(message, ephemeral=tmp)
    except Exception as e:
        print(e)


async def __create_values(stats):
    value_string = ''
    for k, v in stats.items():
        value_string += f'{k}: `{v}`\n'
    return value_string


class Listener(commands.Cog):
    """ This is the Backend class for the Commands, I will expand this section by time """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: nextcord.Interaction):  # Todo Notice
        if str(interaction.type) == 'InteractionType.application_command':
            return

        reaction_id = interaction.data['custom_id']
        if reaction_id == 'csgo':
            username = interaction.message.embeds[0].to_dict()['author']['name']
            user = await self.bot.faceit.get_players(player_name=username)
            stats = await self.bot.faceit.get_player_stats(player_id=user['player_id'])

            csgo_player_data = user['games']['csgo']
            embed = nextcord.Embed(timestamp=self.bot.current_timestamp(),
                                   color=self.bot.faceit_colors[csgo_player_data['skill_level']])

            embed.set_author(name=user['nickname'],
                             icon_url=user['avatar'],
                             url=user['faceit_url'].format(lang=user['country']))

            value_string = await __create_values(stats)

            embed.add_field(name='Spieler Info',
                            value=f'Rank: `{csgo_player_data["skill_level"]}`\n'
                                  f'IG Name: `{csgo_player_data["game_player_name"]}`')

            embed.add_field(name='Spieler Stats',
                            value=value_string,
                            inline=False)

            await interaction.edit_original_message(embed=embed)

        if reaction_id == 'faceit-sync':
            member = interaction.user
            faceit_rank_id = await self.bot.faceit.get_players(member.display_name)

            ch = self.bot.get_channel(interaction.channel_id)

            if not isinstance(faceit_rank_id, dict):
                m: nextcord.Message = await ch.send(
                    f'{member.mention} dein name ist nicht bei Faceit eingetragen, bitte stelle sicher das dein Name richtig ist')
                return await m.delete(delay=5)

            role_name = f'SkillLevel{faceit_rank_id["games"]["csgo"]["skill_level"]}'
            guild = self.bot.get_guild(interaction.guild.id)
            role = nextcord.utils.get(guild.roles, name=role_name)

            await member.add_roles(role)

        if reaction_id in self.bot.emotes.keys():

            member = interaction.user
            roles: list = member.roles

            role_name: str = reaction_id

            guild = self.bot.get_guild(interaction.guild.id)
            role = nextcord.utils.get(guild.roles, name=role_name)

            if role not in roles:
                await send_interaction_msg(f'Der Agent `{reaction_id}` wurde dir hinzugefügt', interaction)
                return await member.add_roles(role)
            await send_interaction_msg(f'Der Agent `{reaction_id}` wurde dir entfernt', interaction)
            return await member.remove_roles(role)


def setup(bot):
    bot.add_cog(Listener(bot))

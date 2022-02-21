import nextcord
from cogs.etc.embeds import help_site
from nextcord import ButtonStyle
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions
from nextcord.ui import View, Button


# todo:
# on restart the thing


async def send_interaction_msg(message: str, interaction: nextcord.Interaction, tmp=True):
    try:
        await interaction.followup.send(message, ephemeral=tmp)
    except Exception as e:
        print('interaction failed', e)


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.valid_channel = [939179519955320902, 939179547449000006, 799010601270509578]
        self.AGENT_CH = 939179519955320902
        self.ch = None

        self.ranks = {  # All ranks in Valorant are listed here
            'iron': {
                'Eisen1': '<:Eisen1:940594881951301683>',
                'Eisen2': '<:Eisen2:940594882454618192>',
                'Eisen3': '<:Eisen3:940594882123292713>', },
            'bronze': {
                'Bronze1': '<:Bronze1:940594881934532708>',
                'Bronze2': '<:Bronze2:940594881867448362>',
                'Bronze3': '<:Bronze3:940594881825476660>', },
            'silver': {
                'Silber1': '<:Silber1:940594882232324106>',
                'Silber2': '<:Silber2:940594882307846194>',
                'Silber3': '<:Silber3:940594882899226634>', },
            'gold': {
                'Gold1': '<:Gold1:940594882010026056>',
                'Gold2': '<:Gold2:940594882316234833>',
                'Gold3': '<:Gold3:940594882823720970>',
            },
            'platin': {
                'Platin1': '<:Platin1:940594882320404520>',
                'Platin2': '<:Platin2:940594882131664896>',
                'Platin3': '<:Platin3:940594882500788264>',
            },
            'diamond': {
                'Diamant1': '<:Diamant1:940594881833881621>',
                'Diamant2': '<:Diamant2:940594881993252895>',
                'Diamant3': '<:Diamant3:940594882458837002>',
            },
            'immortal': {
                'Immortal1': '<:Immortal1:940594882307829841>',
                'Immortal2': '<:Immortal2:940594882735669328>',
                'Immortal3': '<:Immortal3:940594882760806420>',
            },
            'radiant': {'radiant': '<:Radiant:940594882387517491>', }
        }

        self.emotes = {
            'Astra': '<:Astra:940535357768863784>',
            'Killjoy': '<:Killjoy:940535529773080627>',
            'Brimstone': '<:Brimstone:940535426727428126>',
            'Raze': '<:Raze:940535613420077086>',
            'Reyna': '<:Reyna:940535647884693524>',
            'Breach': '<:Breach:940535401549021254>',
            'Yoru': '<:Yoru:940535770341572650>',
            'Skye': '<:Skye:940535693455818772>',
            'Phoenix': '<:Phoenix:940535590443700245>',
            'Chamber': '<:Chamber:940535452614676480>',
            'Viper': '<:Viper:940535750619963392>',
            'Cypher': '<:Cypher:940535468745957397>',
            'Kayo': '<:Kayo:940535510932267028>',
            'Jett': '<:Jett:940535488085909504>',
            'Omen': '<:Omen:940535567937048576>',
            'Sova': '<:Sova:940535719041069106>',
            'Neon': '<:Neon:940535547481440286>',
            'Sage': '<:Sage:940535669908979732>'
        }

        self.embed_content_type = {
            '1': {
                'Iron': {
                    'title': 'Eisen 1 | Eisen 2 | Eisen 3',
                    'ranks': self.ranks['iron']
                },
                'Bronze': {
                    'title': 'Bronze 1 | Bronze 2 | Bronze 3',
                    'ranks': self.ranks['bronze']
                },
                'Silver': {
                    'title': 'Silber 1 | Silber 2 | Silber 3',
                    'ranks': self.ranks['silver']
                },
                'Gold': {
                    'title': 'Gold 1 | Gold 2 | Gold 3',
                    'ranks': self.ranks['gold']
                },
                'Platin': {
                    'title': 'Platin 1 | Platin 2 | Platin 3',
                    'ranks': self.ranks['platin']
                },
                'Diamond': {
                    'title': 'Diamant 1 | Diamant 2 | Diamant 3',
                    'ranks': self.ranks['diamond']
                },
                'Immortal': {
                    'title': 'Immortal 1 | Immortal 2 | Immortal 3',
                    'ranks': self.ranks['immortal']
                },
                'Radiant': {
                    'title': 'Radiant',
                    'ranks': self.ranks['radiant']
                }
            },
            '2': {
                'list': self.emotes,
                'title': 'Wähle dein Agent',
                'description': 'Per Rechtsklick auf die gewünschte Reaktionen werden dir deine Agenten hinzugefügt. Solltest du deine Agenten wechseln wollen, dann drück erneut auf sie, damit diese dann wieder entfernt werden!'
            }
        }

    @commands.Cog.listener()
    async def on_ready(self):  # Here is work, it should be able to create the view new without sending a new message
        ect = self.embed_content_type['2']

        await self.agent_selector_msg(ect)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 942082659885146133:
            if 'MessageType.premium_guild' in str(message.type):
                await self.ch.send(f'{message.author.name} hat den Server geboosted, Danke :)')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.ch.send(
            f'{member.name} ist dem Server beigetreten. Willkommen im Rift')  # Maybe insert here Mention without ping

    @commands.group(no_pm=True)
    @has_permissions(administrator=True)
    async def selfrole(self, ctx):
        msg_len = len(ctx.message.content.split())
        if msg_len == 1:
            return await ctx.send(embed=await help_site('betrayedrift'))

    @selfrole.command(no_pm=True)
    async def agent(self, ctx):
        ect = self.embed_content_type['2']
        return await self.agent_selector_msg(ect)

    @selfrole.command(no_pm=True)
    async def rank(self, ctx):
        ect = self.embed_content_type['1']

        for rank in ect:
            e = nextcord.Embed(title=ect[rank]['title'],
                               color=self.bot.embed_st,
                               timestamp=self.bot.current_timestamp)

            m = await ctx.send(embed=e)

            await self.add_reactions_to_rank_message(ect, m, rank)

    async def add_reactions_to_rank_message(self, ect, m, rank):
        """ Adds needed reaction to ranks embeds message

        :param ect: embed_content_type -> Dictionary get from self.embed_content_type
        :type ect: Dict
        :param m: message
        :param rank: the current rank
        :return: -
        """
        for emote in ect[rank]['ranks']:
            await m.add_reaction(ect[rank]['ranks'][emote])

    async def agent_selector_msg(self, ect):
        """ Creates the agent selector Embed and send it Automatically

        :param ect: embed content type -> Dictionary get from self.embed_content_type
        :type ect: dict
        :return: -
        :rtype: -
        """
        e = nextcord.Embed(title=ect['title'],
                           description=ect['description'],
                           color=self.bot.embed_st,
                           timestamp=self.bot.current_timestamp)

        view = await self.create_view(ect)
        ch = self.bot.get_channel(self.AGENT_CH)

        await ch.purge()
        return await ch.send(embed=e, view=view)

    async def create_view(self, ect) -> View:
        """ Creates a view

        :param ect: embed content type -> Dictionary get from self.embed_content_type
        :type ect: Dict
        :return: ViewObject
        :rtype: Object
        """
        view = View(timeout=None)
        for key in ect['list']:
            view.add_item(Button(label=key, style=ButtonStyle.blurple, emoji=ect['list'][key], custom_id=key))
        return view

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return

        if payload.channel_id not in self.valid_channel:
            return

        member = payload.member
        roles: list = member.roles
        role_name: str = 'Followers'

        if not payload.emoji.name == '✅':
            role_name: str = payload.emoji.name

        guild = self.bot.get_guild(payload.guild_id)
        role = nextcord.utils.get(guild.roles, name=role_name)

        if payload.emoji.name == '✅':
            return await member.add_roles(role)

        ch = self.bot.get_channel(payload.channel_id)
        message = await ch.fetch_message(payload.message_id)
        await message.remove_reaction(payload.emoji, member)

        if role not in roles:
            return await member.add_roles(role)
        await member.remove_roles(role)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: nextcord.Interaction):  # Todo Notice
        if str(interaction.type) == 'InteractionType.application_command':
            return

        reaction_id = interaction.data['custom_id']
        if reaction_id in self.emotes.keys():

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

        if reaction_id == 'csgo':
            print(interaction.message)


def setup(bot):
    bot.add_cog(Roles(bot))

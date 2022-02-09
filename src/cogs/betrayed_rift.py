import nextcord
from cogs.etc.config import EMBED_ST
from cogs.etc.config import current_timestamp
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.valid_channel = [939179519955320902, 939179547449000006]

        self.ranks = {
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
                'Silver':{
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

    @commands.Command
    @has_permissions(administrator=True)
    async def selfrole(self, ctx, msg_type):
        if msg_type not in ['1', '2']:
            return await ctx.send('Invalid msg_type. Possible [1, 2]')

        ect = self.embed_content_type[msg_type]

        if msg_type == '1':  # Extract it too
            for rank in ect:
                e = nextcord.Embed(title=ect[rank]['title'],
                                    color=EMBED_ST,
                                    timestamp=current_timestamp())
                
                m = await ctx.send(embed=e)
                
                for emote in ect[rank]['ranks']:
                    # print(ect[rank]['ranks'][emote])
                    await m.add_reaction(ect[rank]['ranks'][emote])

        if msg_type == '2':  # Extract function

            e = nextcord.Embed(title=ect['title'],
                            description=ect['description'],
                            color=EMBED_ST,
                            timestamp=current_timestamp())

            message = await ctx.send(embed=e)

            for key in ect['list']:
                await message.add_reaction(ect['list'][key])

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # <RawReactionActionEvent message_id=940555116665253898 user_id=327140448638599168
        #   channel_id=799010601270509579 guild_id=797891536746315808
        # emoji=<PartialEmoji animated=False name='viper' id=940535750619963392>
        # event_type='REACTION_ADD'
        # member=<Member id=327140448638599168 name="exersalza[>'-']>" discriminator='1337' bot=False nick=None
        # guild=<Guild id=797891536746315808 name='betrayed Rift' shard_id=0 chunked=True member_count=67>>>

        if payload.member.bot:
            return

        if payload.channel_id not in self.valid_channel:
            return

        member = payload.member
        roles: list = member.roles

        guild = self.bot.get_guild(payload.guild_id)
        role = nextcord.utils.get(guild.roles, name=payload.emoji.name)

        ch = self.bot.get_channel(payload.channel_id)
        message = await ch.fetch_message(payload.message_id)
        await message.remove_reaction(payload.emoji, member)

        if role not in roles:
            return await member.add_roles(role)
        await member.remove_roles(role)


def setup(bot):
    bot.add_cog(Roles(bot))

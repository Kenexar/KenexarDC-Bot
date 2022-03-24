import random

import requests

import nextcord
from nextcord import TextInputStyle, InteractionType
from nextcord.ext import commands
from nextcord.ui import View, Button, Modal, TextInput
from utils import filler


async def is_valid_domain(domain: str) -> bool:
    return True if 'https://docs.google.com/document' in domain else False


async def is_accessible(link: str) -> bool:
    res = requests.get(link)
    if res.status_code != 200:
        return False
    return True if not res.headers.get('X-Frame-Options') else False


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.serverid = 942103043955105892
        self.rank_channelid = 942103044840099907

        self.romes_number = {
            1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V'
        }

        self.ranks = {
            'Iron': {
                'count': 4,
                'emoji': '<:Iron:945601410521772052>',
                'colorcode': 0xfff
            },
            'Bronze': {
                'count': 4,
                'emoji': '<:Bronze:945601409036988437>',
                'colorcode': 0xfff
            },
            'Silber': {
                'count': 4,
                'emoji': '<:Silber:945601409309610014>',
                'colorcode': 0xfff
            },
            'Gold': {
                'count': 4,
                'emoji': '<:Gold:945601409221554206>',
                'colorcode': 0xfff
            },
            'Platin': {
                'count': 4,
                'emoji': '<:Platin:945601409343193118>',
                'colorcode': 0xfff
            },
            'Diamant': {
                'count': 4,
                'emoji': '<:Diamant:945601409351569428>',
                'colorcode': 0xfff
            },
            'Master': {
                'count': 1,
                'emoji': '<:Master:945601409489960960>',
                'colorcode': 0xfff
            },
            'GrandMaster': {
                'count': 1,
                'emoji': '<:GrandMaster:945601410005876797>',
                'colorcode': 0xfff
            },
            'Challenger': {
                'count': 1,
                'emoji': '<:Challenger:945601410345623593>',
                'colorcode': 0xfff
            },
        }

        self.cursed_list = {
            'test': 't̴e̶s̸t̶',
            'ludwig': 'L̸u̸d̶w̸i̷g̵',
            'historyv': 'h̸i̴s̶t̸o̵r̶y̵v̶',
            'till': 'T̸i̸l̶l̵',
            'lakker': 'l̴a̷k̴k̶e̶r̷',
            'twitch': 'T̷w̸i̷t̷c̷h̵',
            'burak': 'b̸u̵r̸a̸k̵',
            'yeet': 'y̶e̶e̶t̷',
        }

        self.verify_user = {}

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.logger.info('Ready, pls don\'t delete me :(')
        self.bot.logger.info(f'Current Shards: {self.bot.cur_shards}')
        self.bot.server_settings = await filler(self.bot)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        pass

    @commands.Command
    async def get_avat(self, ctx: commands.Context, member: str = None):
        if member is not None:
            user = ctx.guild.get_member(int(member.strip('<@&!>')))

    @commands.Command
    async def send_test(self, ctx):
        embed = nextcord.Embed(title=f'\u200b')
        embed.add_field(name=f'\u200b', value=f'\u200b')

        view = View()
        view.add_item(Button(label='test', custom_id='test'))
        view.add_item(Button(label='test2', custom_id='test2'))

        await ctx.send(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_interaction(self, inter: nextcord.Interaction):
        c_id = inter.data.get('custom_id')

        if c_id == 'test2':
            modal = Modal(title='Verification', custom_id='verify-modal')
            choice = random.choice(list(self.cursed_list.keys()))
            word = self.cursed_list.get(choice, "test")

            self.verify_user[inter.user.id] = choice

            modal.add_item(TextInput(label=f'{word} - Captcha', custom_id='Tests'))
            await inter.response.send_modal(modal)
            return

        if c_id == 'test':
            modal = Modal(title=f'Team Bewerbung.', custom_id='team-app')
            modal.add_item(TextInput(label='Wie alt bist du?', custom_id='team-app-1', placeholder='17'))

            modal.add_item(TextInput(label='Wie heißt du?',
                                     custom_id='team-app-3', style=TextInputStyle.paragraph,
                                     placeholder='Name OOC, Name IC', max_length=2048))

            modal.add_item(TextInput(label='Wie sind deine Online zeiten?',
                                     custom_id='team-app-4', style=TextInputStyle.paragraph,
                                     placeholder='Mo-Fr: 10-22 uhr...'))

            modal.add_item(TextInput(label='Google Docs link',
                                     placeholder='Bitte nur die Sachen reinschreiben, die nicht hier Abgefragt werden.',
                                     custom_id='team-app-2'))

            await inter.response.send_modal(modal=modal)
            return

        if c_id == 'team-app':
            comp = inter.data.get('components')

            team_app_1 = comp[0]['components'][0]['value']  # Age
            team_app_2 = comp[1]['components'][0]['value']  # Name
            team_app_3 = comp[2]['components'][0]['value']  # Online times
            team_app_4 = comp[3]['components'][0]['value']  # Link

            if not await is_valid_domain(team_app_4):
                await inter.channel.send(f'{inter.user.mention} Die URL ist keine Google Docs url. Bitte schreibe dein Bewerbung in Google Docs und stelle sicher, dass das Dokument öffentlich ist.\nDu kannst das Formular dann einfach nochmal Ausfüllen.',
                                         delete_after=20)
                return

            if not await is_accessible(team_app_4):
                await inter.channel.send(f'{inter.user.mention} Dein Google Docs dokument ist nicht Öffentlich, du kannst das unter `Freigeben` ändern.',
                                         delete_after=20)
                return

            embed = nextcord.Embed(title=f'Team bewerbung von {inter.user.name}',
                                   color=self.bot.embed_st,
                                   timestamp=self.bot.current_timestamp())

            embed.add_field(name='Alter:', value=team_app_1, inline=False)
            embed.add_field(name='Name:', value=team_app_2, inline=False)
            embed.add_field(name='Online Zeiten:', value=team_app_3, inline=False)
            embed.add_field(name='Docs:', value=f'[__Link__]({team_app_4})', inline=False)
            await inter.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Test(bot))

from datetime import datetime

import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import CommandNotFound
from nextcord.ui import View, Select
from utils import filler

from PIL import Image, ImageDraw, ImageFont


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

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.logger.info('Ready, pls don\'t delete me :(')
        self.bot.logger.info(f'Current Shards: {self.bot.cur_shards}')
        self.bot.server_settings = await filler(self.bot)
        self.bot.dispatch('ticket_startup')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        pass

    @commands.Cog.listener()
    async def on_ticket_startup(self):
        print(self.__class__)

    @commands.Command
    async def get_avat(self, ctx: commands.Context, member: str = None):
        if member is not None:
            user = ctx.guild.get_member(int(member.strip('<@&!>')))

    @commands.Command
    async def send_test(self, ctx):
        embed = nextcord.Embed(title=f'{datetime.now().strftime("%Y-%m-%d%H:%M:%S")}')
        print(self.bot.server_settings)
        embed.add_field(name=f'\u200b', value=f'`{datetime.now().strftime("%Y-%m-%d%H:%M:%S")}`')

        view = View()

        select = Select(custom_id='test')
        select.add_option(label='test', value='missing')
        select.add_option(label='test', value='mi')
        select.add_option(label='test', value='mis')
        select.add_option(label='test', value='miss')
        select.add_option(label='test', value='missi')
        select.add_option(label='test', value='missin')

        view.add_item(select)
        await ctx.send(embed=embed, view=view)


def setup(bot):
    bot.add_cog(Test(bot))

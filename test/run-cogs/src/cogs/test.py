import mysql.connector.connection
import nextcord
from nextcord import ButtonStyle
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions
from nextcord.ui import Button, Item
from nextcord.ui import View


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
        print('ready, pls dont delete me :(')

    @commands.Command
    @has_permissions(administrator=True)
    async def create(self, ctx: commands.Context, category: str = None):
        """

        :param ctx:
        :type ctx:
        :param category:
        :type category:
        :return:
        :rtype:
        """
        if category and category.isdigit():
            ch: nextcord.CategoryChannel = self.bot.get_channel(int(category))

            if str(ch.type) == 'category':
                cur = self.bot.dbBase.cursor(buffered=True)
                if len(ch.voice_channels) >= 4:
                    ch_list = ch.voice_channels[:4]
                    cur.execute("SELECT channel_id FROM dcbots.serverchannel WHERE server_id=%s and not channel_type >= 5",
                                          (ctx.guild.id,))

                    fetcher = cur.fetchall()

                    for channel_id in enumerate(ch_list):
                        sql_string = "INSERT INTO dcbots.serverchannel(server_id, channel_id, channel_type) VALUES (%s, %s, %s)"
                        if fetcher:
                            sql_string = "UPDATE dcbots.serverchannel SET channel_id=%s WHERE server_id=%s AND channel_type=%s"
                        cur.execute(sql_string,
                                    (ctx.guild.id, channel_id[1].id, int(channel_id[0] + 1)))
                    self.bot.dbBase.commit()
                    cur.close()
                try:
                    cur.close()
                except Exception:
                    pass

    @commands.Command
    async def list_all_commands(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Test(bot))

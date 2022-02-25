from nextcord.ext import commands
from nextcord.ext.commands import CommandNotFound


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

    async def filler(self) -> dict:
        cur = self.bot.dbBase.cursor(buffered=True)

        cur.execute("SHOW columns FROM dcbots.server_settings")
        columns_fetcher = cur.fetchall()

        columns = []
        ret = {}

        for column in columns_fetcher:
            if not column[0] == 'id':
                columns.append(column[0])

        cur.execute("SELECT %s FROM dcbots.server_settings" % (', '.join(columns),))
        fetcher = cur.fetchall()
        cur.close()

        for k, *v in fetcher:
            ret[k] = dict(zip(columns[1:], v))

        return ret

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.logger.info('Ready, pls don\'t delete me :(')
        self.bot.server_settings = await self.filler()


def setup(bot):
    bot.add_cog(Test(bot))

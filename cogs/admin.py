from cogs.etc.config import dbBase, CUR, ESCAPE, DBESSENT
from datetime import datetime
from nextcord.ext import commands
from datetime import datetime

from etc.config import ESCAPE
from nextcord.ext import CommandNotFound

from embeds import user_info

#todo:
#   get, del, add, clear
#       getUser
#       getVehicleTrunk
#       delUser
#       delVehicles
#       delWeapon
#       clearWeapons
#       clearInventory
#       clearVehicleTrunk
#       clearUserMoney
#       addUserMoney


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Ready at {datetime.now().strftime("%H:%M:%S")}')


    @commands.command()
    async def get(self, ctx, *args):
        CUR.execute(DBESSENT)

        options = ['user', 'u',
                   'vehtrunk', 'vt',
                   'null']

        if len(args):
            for i in args:
                print(i)

    @commands.command()
    async def delete(self, ctx, *args):
        pass

    @commands.command()
    async def add(self, ctx, *args):
        pass

    @commands.command()
    async def clear(self, ctx, *args):
        pass


def setup(bot):
    bot.add_cog(Admin(bot))

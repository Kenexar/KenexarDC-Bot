from datetime import datetime

from nextcord.ext import commands
from nextcord.ext.commands import CommandNotFound

from cogs.etc.config import ESCAPE
from cogs.etc.embeds import user_info


# todo:
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

    @commands.Cog.listener()
    async def on_command_error(self, ctx,
                               error):  # Function doing intense computing!
        if isinstance(error, CommandNotFound):
            return await ctx.send("Command/API not found.")
        raise error

    @staticmethod
    def parser(rounds, toParse, option) -> list or None:
        """ This is a small self written Argparser

        This Function parse given Arguments for administration

        :param rounds: Insert the max number of words for the return
        :param toParse: Gives the Arg to Parse
        :param option: Insert option for parsing


        :return: list
        """
        return_list = []

        if ESCAPE + toParse in option:
            for i in range(rounds):
                return_list.append(i)
            return return_list
        return None

    @commands.command()
    async def get(self, ctx, *args):
        options = [
            f'{ESCAPE}user', f'{ESCAPE}u',
            f'{ESCAPE}vehicletrunk', f'{ESCAPE}vh', 'Null']

        await ctx.send(embed=user_info(username='test', license='coggers', cash=200, bank=2000, bm=20000, veh=2,
                                       weapons=['carbine: 255/255'], inv={'handy': '1'}))

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

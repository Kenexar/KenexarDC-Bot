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

    @commands.Cog.listener()
    async def on_command_error(self, ctx,
                               error):  # Function doing intense computing!
        if isinstance(error, CommandNotFound):
            return await ctx.send("Command/API not found.")
        raise error

    def parser(rounds, toparse, option) -> list or None:
        '''This is a small self written Argparser
		
		This Function parse given Arguments for administration

		:param rounds: Insert the max number of words for the return
		:param toparse: Gives the Arg to Parse
		:param option: Insert option for parsing


		:return: list
		'''
        return_list = []

        if ESCAPE + toparse in option:
            for i in range(rounds):
                return_list.append(i)
            return return_list
        return None

    @commands.command()
    async def get(self, ctx, *args):
        options = [
            f'{ESCAPE}user', f'{ESCAPE}u', 
			f'{ESCAPE}vehicletrunk', f'{ESCAPE}vh']

    @commands.command()
    async def delete(self, ctx):
        pass

    @commands.command()
    async def add(self, ctx):
        pass

    @commands.command()
    async def clear(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Admin(bot))

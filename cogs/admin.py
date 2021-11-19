from nextcord.ext import commands
from datetime import datetime

from etc.config import ESCAPE

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


	def parser(rounds, toparse, options=list) -> list:
		return_list = []
		
		if ESCAPE + toparse in options:
			for i in range(rounds):
				pass

	@commands.command()
	async def get(self, ctx, *args):
		options = [f'{ESCAPE}user', f'{ESCAPE}u',
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

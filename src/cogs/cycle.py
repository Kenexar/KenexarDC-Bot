import nextcord
import platform

from itertools import cycle
from nextcord.ext import commands, tasks

from cogs.etc.config import dbBase, dbSun
from cogs.etc.config import status_query
from cogs.etc.config import fetch_whitelist

from cogs.etc.presets import Preset


class Cycle(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.whitelist = fetch_whitelist()

		self.status_list = []
		self.status = cycle(status_query(self.status_list))

	@commands.Cog.listener()
	async def on_ready(self):
		
		if platform.system() == 'Linux':
			await self.status_task.start()


	@tasks.loop(seconds=30)
	async def status_task(self):
		await self.bot.change_presence(status=nextcord.Status.online, 
							activity=nextcord.Activity(type=nextcord.ActivityType.watching, 
							name=next(self.status)))

def setup(bot):
	bot.add_cog(Cycle(bot))

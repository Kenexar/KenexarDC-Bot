import nextcord

from itertools import cycle
from nextcord.ext import commands, tasks

from cogs.etc.config import cur
from cogs.etc.config import dbBase
from cogs.etc.config import cur_db
from cogs.etc.config import status_query
from cogs.etc.config import fetch_whitelist

from cogs.etc.presets import Preset


class Cycle(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.whitelist = fetch_whitelist()

		self.status_list = []
		self.status = cycle(status_query(self.status_list))

		self.CYCLE_OPTIONS = [
			'add', 
			'remove', 'rm',
			'list', 'ls',
			'rl', 'reload'
		]

	@commands.Cog.listener()
	async def on_ready(self):
		await self.status_task.start()


	@tasks.loop(seconds=30)
	async def status_task(self):
		await self.bot.change_presence(status=nextcord.Status.online, 
							activity=nextcord.Activity(type=nextcord.ActivityType.watching, 
							name=next(self.status)))

	@commands.Command
	async def cycle(self, ctx, *args):
		if ctx.message.author.id in self.whitelist:
			if not Preset.get_perm(ctx.message.author.id) >= 6:
				print('coggesr')
		return await ctx.send('You are not Authorized to Manage the Bot Status menu!')


def setup(bot):
	bot.add_cog(Cycle(bot))
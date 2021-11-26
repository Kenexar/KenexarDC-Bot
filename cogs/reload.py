import nextcord

from nextcord.ext import commands
from cogs.etc.config import CUR
from cogs.etc.config import whitelist

from cogs.etc.presets import Preset

class Reload(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		self.ids = whitelist

	@commands.Command
	async def whitelist(self, ctx):
		if not ctx.message.author.id in self.ids:
			return await ctx.send('You don\'t have permission to manage the Whitelist')

		check = Preset.parser()

		print(Preset.whitelist('add', ))


def setup(bot):
	bot.add_cog(Reload(bot))

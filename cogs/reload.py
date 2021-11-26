import nextcord

from nextcord.ext import commands
from cogs.etc.config import CUR

from cogs.etc.presets import Preset

class Reload(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		self.ids = (327140448638599168, )

	@commands.Command
	async def whitelist(self, ctx):
		if not ctx.message.author.id in self.ids:
			return await ctx.send('You don\'t have permission to manage the Whitelist')

		print(Preset.whitelist('ADD'))


def setup(bot):
	bot.add_cog(Reload(bot))

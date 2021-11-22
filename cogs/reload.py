import nextcord

from nextcord.ext import commands
from cogs.etc.config import CUR

from cogs.etc.presets import Preset

class Reload(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		self.ids = (327140448638599168)

	@commands.Command
	async def reload(self, ctx):
		if not ctx.message.author.id in self.ids:
			return await ctx.send('Du bist nicht Berechtigt um Module neu zu starten!')

		print(Preset.whitelist('ADD'))


def setup(bot):
	bot.add_cog(Reload(bot))
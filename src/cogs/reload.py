from nextcord.ext import commands


class Reload(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


def setup(bot):
	bot.add_cog(Reload(bot))

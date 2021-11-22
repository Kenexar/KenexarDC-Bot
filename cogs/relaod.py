import nextcord

from nextcord.ext import commands
from cogs.etc.config import CUR

from cogs.admin.Admin import parser

class Reload(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		self.ids = ()

	@commands.Command
	async def reload(self, ctx):
		if not ctx.message.author.id in self.ids:
			return await ctx.send('Du bist nicht Berechtigt um Module neu zu starten!')

	
	def whitelist(mode, user=nextcord.Member):
		"""Whitelist function whitelist a member
		
		:param mode:add: Add a Member to the Whitelist for Administration
		:param mode:list: List all members on the whitelist
		:param mode:remove: Remove a Member from the Whitelist

		:returns: SQL Insert/Update
		"""
		pass


def setup(bot):
	bot.add_cog(Reload(bot))
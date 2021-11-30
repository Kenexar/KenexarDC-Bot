from nextcord.ext import commands

class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Command
	async def opfer(self, ctx):
		return await ctx.send(f'{ctx.author.mention} maul!')

def setup(bot):
	bot.add_cog(Fun(bot))
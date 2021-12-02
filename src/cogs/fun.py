from nextcord.ext import commands

from src.cogs.etc.rcon import Rcon


class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Command
	async def opfer(self, ctx):
		rcon = Rcon('host', "password")

		# If you don't need a response and
		# don't want to wait 3 sec for the timeout

		response = rcon.send_command("status")
		return await ctx.send(response)

def setup(bot):
	bot.add_cog(Fun(bot))
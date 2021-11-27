import nextcord

from nextcord.ext import commands
from cogs.etc.config import cur
from cogs.etc.config import ESCAPE
from cogs.etc.config import DBBASE
from cogs.etc.config import cur_db
from cogs.etc.config import fetch_whitelist

from cogs.etc.presets import Preset


class Reload(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


def setup(bot):
	bot.add_cog(Reload(bot))

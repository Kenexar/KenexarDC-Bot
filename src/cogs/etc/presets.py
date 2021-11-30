import nextcord

from nextcord import Embed

from cogs.etc.config import EMBED_ST
from cogs.etc.config import PROJECT_NAME
from cogs.etc.config import cur_db
from cogs.etc.config import dbBase
from cogs.etc.config import WHITELIST_RANKS


class Preset:
	""" This is the Main function part for my Administration bot """
	@staticmethod
	def parser(rounds=int, toparse=list, option=list) -> list or str:
		""" This is a small self written Argparser

		This Function parse given Arguments for administration

		:param rounds:int: Insert the max number of words for the return
		:param toparse:list: Gives the Arg to Parse
		:param option:list: Insert option for parsing

		:return: list
		"""

		return_list = []

		for key in toparse:
			if toparse[toparse.index(key)] in option:
				for i in range(rounds):
					try:
						return_list.append(toparse[i])
					except IndexError:
						return 'Index out of range'
				return return_list
			return return_list

	@staticmethod
	def whitelist(mode=str, member=int, rank=int) -> Embed or str:
		"""Whitelist function whitelist a member

		:param mode:str-add: Add a Member to the Whitelist for Administration
		:param mode:str-list: List all members on the whitelist
		:param mode:str-remove: Remove a Member from the Whitelist
		:param member: Serve the member

		:returns: String or nextord.Embed object
		"""

		if mode == 'list':
			cur_db.execute(
			f"SELECT uid, rank FROM whitelist WHERE name='{PROJECT_NAME}'")
			fetcher = cur_db.fetchall()

			embed = nextcord.Embed(title='Whitelist', color=EMBED_ST)

			if fetcher:
				for i in fetcher:
					embed.add_field(name=i[0],
					value=f'Rank: {WHITELIST_RANKS[i[1]]}',
					inline=False)
			else:
				return 'Cannot find any entries'
			return embed

		elif mode == 'add':
			cur_db.execute(
				"INSERT INTO whitelist(name, uid, rank) VALUES (%s, %s, %s)",
				(PROJECT_NAME, member, rank))
			dbBase.commit()
			return f'Added <@{member}> to the [BOT]whitelist'

		elif mode == 'remove':
			cur_db.execute("DELETE FROM whitelist WHERE uid=%s and name=%s;",
				(member, PROJECT_NAME))
			dbBase.commit()
			return f'Removed <@{member}> from [BOT]whitelist'
		else:
			return f'`{mode}` is not available'

	@staticmethod
	def get_perm(user):
		cur_db.execute('SELECT rank FROM whitelist WHERE uid=%s', (user,))
		return cur_db.fetchone()[0]

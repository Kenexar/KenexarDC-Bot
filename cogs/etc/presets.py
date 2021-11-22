import nextcord

from cogs.etc.config import ESCAPE
from cogs.etc.config import CUR
from cogs.etc.config import PROJECT_NAME
from cogs.etc.config import db


class Preset:
	""" This is the Main function part for my Administration bot """
	def parser(self, rounds, toParse, option) -> None:
		""" This is a small self written Argparser
		
		This Function parse given Arguments for administration

		:param rounds: Insert the max number of words for the return
		:param toParse: Gives the Arg to Parse
		:param option: Insert option for parsing

		:return: list
		"""

		return_list = []

		for key in toParse:
			if ESCAPE + toParse[toParse.index(key)] in option:
				for i in range(rounds):
					return_list.append(toParse[i + 1])
				return return_list
			
	

	def whitelist(mode, member=int) -> str or list:
		"""Whitelist function whitelist a member
		
		:param mode:add: Add a Member to the Whitelist for Administration
		:param mode:list: List all members on the whitelist
		:param mode:remove: Remove a Member from the Whitelist

		:returns: SQL Insert/Update
		"""

		if mode == 'list':
			compare = []

			CUR.execute(f"SELECT uid FROM whitelist WHERE name='{PROJECT_NAME}'")
			fetcher = CUR.fetchall()
			
			if fetcher:
				for i in fetcher:
					compare.append(i)
			else:
				return 'Cannot find any entries'
			
			return compare

		elif mode == 'add':
			CUR.execute("INSERT INTO whitelist(name, uid) VALUES (?, ?)", (PROJECT_NAME, member))
			db.commit()
			return f'Added <@{member}> to the whitelist'

		elif mode == 'remove':
			CUR.execute("DELETE FROM whitelist WHERE uid=? and name=?;", (member, PROJECT_NAME))
			db.commit()
			return f'Removed <@{member}> from whitelist'
		else:
			return f'{mode} is not available'
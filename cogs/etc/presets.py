from cogs.etc.config import ESCAPE
from cogs.etc.config import PROJECT_NAME
from cogs.etc.config import cur
from cogs.etc.config import db


class Preset:
	""" This is the Main function part for my Administration bot """
	@staticmethod
	def parser(rounds=int, toparse=list, option=list) -> list:
		""" This is a small self written Argparser

		This Function parse given Arguments for administration

		:param rounds:int: Insert the max number of words for the return, beware the argument
		is not listed
		:param toparse:list: Gives the Arg to Parse
		:param option:list: Insert option for parsing

		:return: list
		"""

		return_list = []

		for key in toparse:
			if ESCAPE + toparse[toparse.index(key)].strip(ESCAPE) in option:
				for i in range(rounds):
					return_list.append(toparse[i])
				return return_list
			return return_list

	@staticmethod
	def whitelist(mode=str, member=int) -> str or list:
		"""Whitelist function whitelist a member

		:param mode:str-add: Add a Member to the Whitelist for Administration
		:param mode:str-list: List all members on the whitelist
		:param mode:str-remove: Remove a Member from the Whitelist
		:param member: Serve the member

		:returns: SQL Insert/Update
		"""

		if mode == 'list':
			compare = []

			cur.execute(f"SELECT uid FROM whitelist WHERE name='{PROJECT_NAME}'")
			fetcher = cur.fetchall()

			if fetcher:
				for i in fetcher:
					compare.append(i)
			else:
				return 'Cannot find any entries'

			return compare

		elif mode == 'add':
			cur.execute("INSERT INTO whitelist(name, uid) VALUES (%s, %s)", (PROJECT_NAME, member))
			db.commit()
			return f'Added <@{member}> to the [BOT]whitelist'

		elif mode == 'remove':
			cur.execute("DELETE FROM whitelist WHERE uid=%s and name=%s;", (member, PROJECT_NAME))
			db.commit()
			return f'Removed <@{member}> from [BOT]whitelist'
		else:
			return f'`{mode}` is not available'

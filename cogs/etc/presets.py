import nextcord

from cogs.etc.config import ESCAPE


class Preset:
	""" This is the Main function part for my Administration bot """
	def parser(self, rounds, toParse, option) -> list or None:
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
			return None
	

	def whitelist(mode):
		"""Whitelist function whitelist a member
		
		:param mode:add: Add a Member to the Whitelist for Administration
		:param mode:list: List all members on the whitelist
		:param mode:remove: Remove a Member from the Whitelist

		:returns: SQL Insert/Update
		"""
		return mode
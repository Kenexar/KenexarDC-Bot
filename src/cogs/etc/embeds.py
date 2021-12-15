from datetime import datetime

from nextcord import Embed

from cogs.etc.config import EMBED_ST, PREFIX


def user_info(user=dict) -> Embed:
	""" An embed for the get user command

	:param user: User takes an dictionairy with harcoded values, that comes from
	a SQL query

	"""

	global s

	username = user.get('username', '-')
	license_ = user.get('license', '-')
	group = user.get('group', '-')

	firstname = user.get('firstname', '-')
	lastname = user.get('lastname', '-')
	phone_number = user.get('phone_number', '-')

	job = user.get('job', '-')
	job_grade = user.get('job_grade', '-')

	cash = user.get('cash', '-')
	bank = user.get('bank', '-')
	bm = user.get('bm', '-')
	veh = user.get('veh', '-')

	weapons = user.get('weapons', '-')
	inv = user.get('inv', '-')

	embed = Embed(title=username,
					description=license_,
					color=EMBED_ST,
					timestamp=datetime.utcnow()) # embed creation

	embed.add_field(name='Information',
					value=f'Group: {group}\n\nVoller Name: {firstname}, {lastname}\nJob: {job}. Grade: {job_grade}\n'
							f'Telefon: {phone_number}'
							f'\n\n💰 Bargeld: {cash}\n💳 Bank: {bank}\n💸 Schwarzgeld: {bm}\n\n🚘 Fahrzeuge: {veh}',
					inline=False)

	if len(weapons):
		f = '\n'.join(weapons)
	else:
		f = 'Hat keine Waffen im Inventar'

	embed.add_field(name='Waffen', value=f, inline=False)

	if len(inv):
		f = '\n'.join(inv)
		s = '\n'.join(str(inv[i]) for i in inv)
	else:
		f = 'Hat keine Items im Inventar'
		s = '\u200b'

	embed.add_field(name='Inventar', value=f, inline=True)
	embed.add_field(name='--', value=s, inline=True)

	return embed


def help_site(mode='all') -> Embed:
	""" Creates an Help embed

	:param mode: Standart is all but you can deliever a argument for the
	help embed that is needed

	:return: nextcord.Embed object
	"""
	embed = Embed(title='Help Site - MrPython',
					timestamp=datetime.utcnow(),
					color=EMBED_ST)

	if mode in ('all', 'whitelist'):
		embed.add_field(name=f'`{PREFIX}whitelist` [list|add|remove]',
						value=f'`Usage`: `{PREFIX}whitelist` [list/add|remove] discord.Member.\n\n'
							f'`Des`: List - Lists all members on the Whitelist. \n'
							f'`Des`: Add/Remove - Adds or Removes a discord.Member.',
						inline=False)

	if mode in ('all', 'einreise'):
		embed.add_field(name=f'`{PREFIX}einreise`',
						value=f'Usage: `{PREFIX}einreise` user id [Cfx]\n\nDes: Delete user entry from database',
						inline=False)

	if str(mode) == 'cadd':
		embed.add_field(name=f'`{PREFIX}cadd`',
						value=f'Usage: `{PREFIX}cadd <Words up to 50 Chars>\n\nDes: Adds something to the Status query',
						inline=False)

	return embed


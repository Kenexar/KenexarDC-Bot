from datetime import datetime

from nextcord import Embed
from cogs.etc.config import EMBED_ST, EMBED_RED, EMBED_GREEN


def user_info(username=str, license=str, cash=int, bank=int, bm=int, veh=int, weapons=dict, inv=dict) -> Embed:
	embed = Embed(title=username, 
					descripton=license, 
					color=EMBED_ST, 
					timestamp=datetime.utcnow())

	embed.add_field(name='Information', 
					value=f'💰Bargeld: {cash}\n💳Bank: {bank}\n💸Schwarzgeld: {bm}\n\n🚘Fahrzeuge: {veh}', 
					inline=False)
	if not len(weapons):
		f = '\n'.join(weapons)
		s = '\n'.join(weapons[i] + '/255' for i in weapons)
	else:
		f = 'Hat keine Waffen im Inventar'

	embed.add_field(name='Waffen', value=f, inline=True)
	embed.add_field(name='--', value=s, inline=False)

	if not len(weapons):
		f = '\n'.join(inv)
		s = '\n'.join(inv[i] for i in inv)
	else:
		f = 'Hat keine Items im Inventar'

	embed.add_field(name='Inventar', value=f, inline=True)
	embed.add_field(name='--', value=s, inline=False)

	return embed

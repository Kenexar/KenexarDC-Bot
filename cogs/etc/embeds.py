from datetime import datetime

from nextcord import Embed

from cogs.etc.config import EMBED_ST


def user_info(username=str, license=str, cash=int, bank=int, bm=int, veh=int, weapons=list, inv=dict) -> Embed:
    global f, s, fi, si
    embed = Embed(title=username,
                  description=license,
                  color=EMBED_ST,
                  timestamp=datetime.utcnow())

    embed.add_field(name='Information',
                    value=f'💰 Bargeld: {cash}\n💳 Bank: {bank}\n💸 Schwarzgeld: {bm}\n\n🚘 Fahrzeuge: {veh}',
                    inline=False)
    if len(weapons):
        print(weapons, inv)
        f = '\n'.join(weapons)
    else:
        f = 'Hat keine Waffen im Inventar'

    embed.add_field(name='Waffen', value=f, inline=False)

    if len(inv):
        fi = '\n'.join(inv)
        si = '\n'.join([inv[i] for i in inv])
    else:
        fi = 'Hat keine Items im Inventar'
        si = '--'

    embed.add_field(name='Inventar', value=fi, inline=True)
    embed.add_field(name='--', value=si, inline=True)

    return embed

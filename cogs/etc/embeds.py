from datetime import datetime

from nextcord import Embed

from cogs.etc.config import EMBED_ST


def user_info(user=dict) -> Embed:
    global f, s, fi, si

    username = user.get('username', None)
    license_ = user.get('license', None)

    cash = user.get('cash', None)
    bank = user.get('bank', None)
    bm = user.get('bm', None)
    veh = user.get('veh', None)

    weapons = user.get('weapons', None)
    inv = user.get('inv', None)

    embed = Embed(title=username,
                  description=license_,
                  color=EMBED_ST,
                  timestamp=datetime.utcnow())

    embed.add_field(name='Information',
                    value=f'Group: \n\n💰 Bargeld: {cash}\n💳 Bank: {bank}\n💸 Schwarzgeld: {bm}\n\n🚘 Fahrzeuge: {veh}',
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

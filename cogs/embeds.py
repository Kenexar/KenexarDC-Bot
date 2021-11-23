from datetime import datetime

from nextcord import Embed

from cogs.etc.config import EMBED_ST


def user_info(user=dict) -> Embed:
    username = user['username']
    license_ = user['license']

    firstname = user['firstname']
    lastname = user['lastname']
    phone = user['phone_number']
    job = user['job']
    job_grade = user['job_grade']

    cash = user['cash']
    bank = user['bank']
    bm = user['bm']

    veh = user['veh']
    weapons = user['weapons']
    inv = user['inv']

    embed = Embed(title=username,
                  description=license_,
                  color=EMBED_ST,
                  timestamp=datetime.utcnow())

    embed.add_field(name='Information',
                    value=f'Vorname: {firstname}\nNachname: {lastname}\nTel: {phone}\nJob: {job}, Grad: {job_grade}'
                          f'💰Bargeld: {cash}\n💳Bank: {bank}\n💸Schwarzgeld: {bm}\n\n🚘Fahrzeuge: {veh}',
                    inline=False)
    if not len(weapons):
        f = '\n'.join(weapons)
        s = '\n'.join(weapons[i] + '/255' for i in weapons)
    else:
        f = 'Hat keine Waffen im Inventar'

    embed.add_field(name='Waffen', value=f, inline=True)
    embed.add_field(name='__//--\\\\__', value=s, inline=False)

    if not len(weapons):
        f = '\n'.join(inv)
        s = '\n'.join(inv[i] for i in inv)
    else:
        f = 'Hat keine Items im Inventar'

    embed.add_field(name='Inventar', value=f, inline=True)
    embed.add_field(name='--', value=s, inline=False)

    return embed

from datetime import datetime

from nextcord import Embed

from cogs.etc.config import EMBED_ST


def user_info(user=dict) -> Embed:
    username = user.get('username')
    license_ = user.get('license')

    firstname = user.get('firstname')
    lastname = user.get('lastname')
    phone = user.get('phone_number')
    job = user.get('job')
    job_grade = user.get('job_grade')

    cash = user.get('cash')
    bank = user.get('bank')
    bm = user.get('bm')

    veh = user.get('veh')
    weapons = user.get('weapons')
    inv = user.get('inv')

    embed = Embed(title=username,
                  description=license_,
                  color=EMBED_ST,
                  timestamp=datetime.utcnow())

    embed.add_field(name='Information',
                    value=f'Vorname: {firstname}\nNachname: {lastname}\nTel: {phone}\nJob: {job}, Grad: {job_grade}'
                          f'💰Bargeld: {cash}\n💳Bank: {bank}\n💸Schwarzgeld: {bm}\n\n🚘Fahrzeuge: {veh}',
                    inline=False)
    if len(weapons):
        f = '\n'.join(weapons)
        s = '\n'.join(weapons[i] + '/255' for i in weapons)
    else:
        f = 'Hat keine Waffen im Inventar'

    embed.add_field(name='Waffen', value=f, inline=True)
    embed.add_field(name='--', value=s, inline=False)

    if len(inv):
        f = '\n'.join(inv)
        s = '\n'.join(inv[i] for i in inv)
    else:
        f = 'Hat keine Items im Inventar'

    embed.add_field(name='Inventar', value=f, inline=True)
    embed.add_field(name='--', value=s, inline=False)

    return embed

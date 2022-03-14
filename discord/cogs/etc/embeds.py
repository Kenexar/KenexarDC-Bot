from cogs.etc.config import EMBED_ST, PREFIX, current_timestamp
from nextcord import Embed


def user_info(user=dict) -> Embed:
    """ Create an User information Embed to send

    :param user: Enter a dict that you gotten from the SQL request from the user db
    :return: An sendable embed for ctx
    """

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
                  timestamp=current_timestamp())  # embed creation

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


async def help_site(mode='user') -> Embed:
    """ Creates a Help embed

    :param mode: Standard is all but you can deliver an argument for the
    help embed that is needed

    :return: nextcord.Embed object
    """
    embed = Embed(title='Help Site - MrPython',
                  timestamp=current_timestamp(),
                  color=EMBED_ST)

    if mode in ('user', 'casino'):
        embed.add_field(name=f'Casino',
                        value=f'`Blackjack:` `{PREFIX}blackjack` (points), alias: `bj`\n'
                              f'`Des`: Play a round of BlackJack (-Currently not available-)',
                        inline=False)

    if mode in ('user', 'MemberCounter', 'full'):
        embed.add_field(name=f'Server stats',
                        value=f'`{PREFIX}create`\n'
                              f'`Des`: Creates a Category with 4 channels inside of. The Bot counts Online, User in Voice, Voice channel and All users on the Discord)',
                        inline=False)

    if mode in ('user', 'jtc', 'full'):
        embed.add_field(name='Join to Create or JTC',
                        value=f'`Des`: When JTC is active, users can join the Created channel,\nwhen they join a channel with there names will be created. After all users left the channel, the channel gets deleted, to keep the Server clean :)\n\n'
                              f'`{PREFIX}channel` [size (0-99)|owner|claim-owner|set-owner (member mention)|name|info] its self explaining\n'
                              f'`{PREFIX}set (channel mention) -> Channel modify rights are here needed`',
                        inline=False)

    if mode in ('credits', 'user', 'full'):
        embed.add_field(name='Credits',
                        value=f'`{PREFIX}Credits` -> Show the credits for the bot',
                        inline=False)

    if mode in ('betrayedrift', 'full'):
        embed.add_field(name='Betrayed Rift - Custom commands',
                        value=f'`{PREFIX}selfrole [1|2] 1: resend rank embeds, 2: resend agent selection`',
                        inline=False)

    if mode in ('mod', 'whitelist', 'full'):
        embed.add_field(name=f'`{PREFIX}whitelist` [list|add|remove]',
                        value=f'`Usage`: `{PREFIX}whitelist` [list/add|remove] discord.Member.\n\n'
                              f'`Des`: List - Lists all members on the Whitelist. \n'
                              f'`Des`: Add/Remove - Adds or Removes a discord.Member.',
                        inline=False)

    if mode in ('mod', 'einreise', 'full'):
        embed.add_field(name=f'`{PREFIX}einreise`',
                        value=f'Usage: `{PREFIX}einreise` user id [Cfx]\n\nDes: Delete user entry from database',
                        inline=False)

    if mode in ('admin', 'cadd', 'full'):
        embed.add_field(name=f'`{PREFIX}cadd`',
                        value=f'Usage: `{PREFIX}cadd <Words up to 50 Chars>\n\nDes: Adds something to the Status query',
                        inline=False)

    if mode in ('admin-reload', 'admin', 'full'):
        embed.add_field(name=f'{PREFIX}listmodules', value='Des: List all current modules in Cogs',
                        inline=False)
        embed.add_field(name=f'{PREFIX}reload (module name)',
                        value=f'Des: Reload giving Cog module\nExample: {PREFIX}reload cogs.casino',
                        inline=False)

    if mode in ('admin-load', 'admin', 'full'):
        embed.add_field(name=f'{PREFIX}listmodules', value='Des: List all Loaded/Unloaded modules in Cogs',
                        inline=False)
        embed.add_field(name=f'{PREFIX}start (module name)',
                        value=f'Des: Loads giving Cog module\nExample: {PREFIX}load cogs.casino',
                        inline=False)

    if mode in ('admin-unload', 'admin', 'full'):
        embed.add_field(name=f'{PREFIX}listmodules', value='Des: List all Loaded/Unloaded modules in Cogs',
                        inline=False)
        embed.add_field(name=f'{PREFIX}stop (module name)',
                        value=f'Des: Unloads giving Cog module\nExample: {PREFIX}unload cogs.casino',
                        inline=False)

    return embed

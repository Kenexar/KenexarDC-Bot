from datetime import datetime

import nextcord
from cogs.etc.config import DBBASE, dbBase
from cogs.etc.config import LOG_CHANNEL, LOG_SERVER
from cogs.etc.config import current_timestamp, EMBED_ST
from cogs.etc.config import fetch_whitelist
from cogs.etc.embeds import help_site
from cogs.etc.presets import whitelist, get_perm
from cogs.logger.logger import logger
from nextcord.ext import commands
from nextcord.ext.commands import CommandNotFound
from nextcord.ext.commands.errors import MissingPermissions


# todo:
#   get, del, add, clear
#       getVehicleTrunk
#		delUser
#       delVehicles
#       delWeapon
#       clearInventory
#       clearVehicleTrunk
#       clearUserMoney
#       addUserMoney
#       whitelist request
#       help permission system


class Admin(commands.Cog):
    """ Admin class for Moderation actions """

    def __init__(self, bot):
        self.bot = bot
        self.whitelist = fetch_whitelist()

        self.guild = None
        self.logger = None

        self.GET_OPTIONS = [
            'user', 'u',
            'vehicletrunk', 'vh', 'Null'
        ]

        self.DEL_OPTIONS = [
            'fuser', 'fu',
            'veh', 'vehicle',
            'vehtrunk', 'veht',
            'usermoney', 'um',
            'inv', 'inventory',
            'weapons', 'Null'
        ]

        self.ADD_OPTIONS = [
            'um', 'usermoney',
            'weapons'
        ]

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'\nReady at {datetime.now().strftime("%H:%M:%S")}')

        for server in self.bot.guilds:
            if server.id == LOG_SERVER:
                self.guild = server
                self.logger = server.get_channel(LOG_CHANNEL)

        print(logger('info', f'Current logger channel: {self.logger.name}'))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):  # Function doing intense computing!
        if isinstance(error, CommandNotFound):  # error handler
            return await ctx.send("Command not found.")

        if isinstance(error, MissingPermissions):
            return await ctx.send('Insufficient permission')
        raise error

    @commands.command(name='whitelist')
    async def _whitelist(self, ctx, *args):
        if ctx.message.author.id not in self.whitelist:
            return await ctx.send('You are not Authorized to manage the Whitelist'), \
                   await self.logger.send(f'{ctx.message.author} tried to use the `whitelist` command!')

        cur_base = dbBase.cursor()
        cur_base.execute(DBBASE)

        id = ctx.message.author.id

        if await get_perm(id) != 5:
            return await ctx.send('You are not Authorized to manage the Whitelist'), \
                   await self.logger.send(f'{ctx.author} tried to use the `whitelist` command!')

        if not args:
            return await ctx.send(embed=help_site('whitelist'))

        if args[0] == 'add':
            payload = {'member': args[1].strip('<!@ >'), 'rank': args[2] if args[2].isdigit() else 0,
                       'name': ctx.author.name}

            return await ctx.send(await whitelist('add', payload, cur_base))
        if args[0] == 'remove':
            payload = {'user': args[1].strip('<!@ >')}

            return await ctx.send(await whitelist('remove', payload, cur_base))
        if args[0] == 'list':
            return await ctx.send(embed=await whitelist('list', 'payload', cur_base))
        return await ctx.send('The argument is not valid!')

    @commands.Command
    async def help(self, ctx):
        await ctx.send(embed=help_site())

    @commands.Command
    async def credits(self, ctx):
        message = """
Creater: exersalza#1337, ZerxDE#8183
Maintained by: exersalza#1337

**Links:**
**Github:** https://github.com/kenexar
**Github:** https://github.com/exersalza
**Github:** https://github.com/ZerXGIT

**Website:** https://kenexar.eu

**Twitch:** https://twitch.tv/exersalza
**Twitch:** https://twitch.tv/ZerXDElive
                """

        embed = nextcord.Embed(title='Credits',
                               description=message,
                               color=EMBED_ST,
                               timestamp=current_timestamp)
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Admin(bot))

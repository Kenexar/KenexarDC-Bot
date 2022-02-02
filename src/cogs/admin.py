from datetime import datetime

from nextcord.ext import commands
from nextcord.ext.commands import CommandNotFound

from src.cogs.etc.config import DBBASE, dbBase
from src.cogs.etc.config import LOG_CHANNEL, LOG_SERVER
from src.cogs.etc.config import fetch_whitelist
from src.cogs.etc.embeds import help_site
from src.cogs.etc.presets import whitelist, get_perm
from src.cogs.logger.logger import logger


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
        raise error

    @commands.Command
    async def whitelist(self, ctx, *args):
        if ctx.message.author.id not in self.whitelist:
            return await ctx.send('You are not Authorized to manage the Whitelist'), \
                   await self.logger.send(f'{ctx.message.author} tried to use the `whitelist` command!')

        cur_base = dbBase.cursor()
        cur_base.execute(DBBASE)

        id = ctx.message.author.id

        if get_perm(id) != 5:
            return await ctx.send('You are not Authorized to manage the Whitelist'), \
                   await self.logger.send(f'{ctx.author} tried to use the `whitelist` command!')

        if not args:
            return await ctx.send(embed=help_site('whitelist'))

        if args[0] == 'add':
            payload = {'member': args[1].strip('<!@ >'), 'rank': args[2] if args[2].isdigit() else 0,
                       'name': ctx.author.name}

            return await ctx.send(whitelist('add', payload, cur_base))
        if args[0] == 'remove':
            payload = {'user': args[1].strip('<!@ >')}

            return await ctx.send(whitelist('remove', payload, cur_base))
        if args[0] == 'list':
            return await ctx.send(embed=whitelist('list', 'payload', cur_base))
        return await ctx.send('The argument is not valid!')

    @commands.Command
    async def help(self, ctx):
        await ctx.send(embed=help_site())


def setup(bot):
    bot.add_cog(Admin(bot))

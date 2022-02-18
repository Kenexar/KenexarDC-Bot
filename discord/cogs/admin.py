from datetime import datetime

import nextcord
from cogs.etc.embeds import help_site
from cogs.etc.presets import whitelist, get_perm
from cogs.logger.logger import logger
from nextcord.ext import commands
from nextcord.ext.commands import CommandNotFound
from nextcord.ext.commands.errors import MissingPermissions


class Admin(commands.Cog):
    """ Admin class for Moderation actions """

    def __init__(self, bot):
        self.bot = bot
        self.whitelist = self.bot.fetch_whitelist

        self.guild = None
        self.logger = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'\nReady at {datetime.now().strftime("%H:%M:%S - %d.%m.%y")}')

        for server in self.bot.guilds:
            if server.id == self.bot.log_server:
                self.guild = server
                self.logger = server.get_channel(self.bot.log_channel)

        print(logger('info', f'Current logger channel: {self.logger.name}'))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):  # Function doing intense computing!
        if isinstance(error, CommandNotFound):  # error handler
            return await ctx.send("Command not found.")

        if isinstance(error, MissingPermissions):
            return await ctx.send('Insufficient permission')

        if isinstance(error, nextcord.errors.NotFound):
            return

        ch = self.bot.get_channel(self.bot.log_channel)
        err_message = f"""{error}\n<@{self.bot.authorid}>"""
        return await ch.send(err_message)

    @commands.command(name='whitelist')
    async def _whitelist(self, ctx, *args):
        """ Configure the whitelist settings,

        :param ctx: -
        :type ctx: context.Context
        :param args:
        :type args: Sequence[str]
        :return: None
        :rtype:
        """
        if ctx.message.author.id not in self.whitelist:
            return await ctx.send('You are not Authorized to manage the Whitelist'), \
                   await self.logger.send(f'{ctx.message.author} tried to use the `whitelist` command!')

        cur_base = self.bot.dbBase.cursor()
        cur_base.execute("use dcbots;")

        uid = ctx.message.author.id

        if await get_perm(uid) != 5:
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

    # @nextcord.slash_command(name='help', description='Show the help site for the Bot', force_global=True, guild_ids=[])
    @commands.Command
    async def help(self, ctx: commands.Context):
        if ctx.author.id == self.bot.authorid:
            await ctx.send(embed=await help_site('full'))
            return
        await ctx.send(embed=await help_site())

    # @nextcord.slash_command(name='credits', description='Show the credits for the Bot', guild_ids=[], force_global=True)
    @commands.Command
    async def credits(self, ctx: commands.Context):
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
                               color=self.bot.embed_st,
                               timestamp=self.bot.current_timestamp)
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Admin(bot))

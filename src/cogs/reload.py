import asyncio
import os

import nextcord
from cogs.etc.embeds import help_site
from nextcord.ext import commands
from nextcord.ext.commands import CommandNotFound

names = ['__init__.py', 'playground.py', 'gtarp_stuff.py']


async def current_cog_modules(unloaded: list) -> list:
    current_modules = []
    for f in os.listdir('cogs'):
        if f.endswith(".py") and f not in names:
            if f not in unloaded:
                current_modules.append('cogs.' + f[:-3])
    return current_modules


class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.unloaded_modules = []

    @commands.Command
    async def stop(self, ctx, cog_module=None):
        if not ctx.author.id == self.bot.authorid:
            return CommandNotFound()

        if not cog_module:
            return await ctx.send(embed=help_site('admin-unload'))

        if cog_module in await current_cog_modules(self.unloaded_modules):
            return await ctx.send('The giving module is already unloaded!')

        self.unloaded_modules.append(cog_module)

        self.bot.unload_extension(cog_module)
        await ctx.send(f'{cog_module} successfully unloaded')

    @commands.Command
    async def start(self, ctx, cog_module=None):
        if not ctx.author.id == self.bot.authorid:
            return CommandNotFound()

        if not cog_module:
            return await ctx.send(embed=help_site('admin-load'))

        if cog_module not in await current_cog_modules(self.unloaded_modules):
            return await ctx.send('The giving module is already loaded!')

        self.unloaded_modules.remove(cog_module)

        self.bot.load_extension(cog_module)
        await ctx.send(f'{cog_module} successfully loaded')

    @commands.Command
    async def reload(self, ctx, cog_module=None):
        if not ctx.author.id == self.bot.authorid:
            return CommandNotFound()

        if not cog_module:
            return await ctx.send(embed=help_site('admin-reload'))

        if cog_module in self.unloaded_modules:
            return await ctx.send('The giving module is not Loaded!')

        self.bot.unload_extension(cog_module)
        await asyncio.sleep(1)

        self.bot.load_extension(cog_module)
        await ctx.send(f'{cog_module} Reloaded!')

    @commands.Command
    async def listmodules(self, ctx):
        if not ctx.author.id == self.bot.authorid:
            return CommandNotFound()

        embed = nextcord.Embed(title='All Cogs that are loaded are listed here!',
                               color=self.bot.embed_st,
                               timestamp=self.bot.current_timestamp)

        unloaded = '\n'.join(
            self.unloaded_modules) if self.unloaded_modules else 'All modules running down da street, i here AH AH AH AH '

        embed.add_field(name='Loaded Modules', value='\n'.join(await current_cog_modules(self.unloaded_modules)),
                        inline=False)
        embed.add_field(name='Unloaded Modules', value=unloaded, inline=False)

        embed.add_field(name=f'To reload cog modules, write `{self.bot.prefix}reload (cog_module)`',
                        value=f'Example: `{self.bot.prefix}reload cogs.casino`',
                        inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Reload(bot))

import os
from datetime import datetime
from datetime import timedelta

import nextcord
from nextcord.ext import tasks
from nextcord.ext import commands
from nextcord.ext.commands import CommandNotFound


class AutoModuleReloader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.changed_modules = []

        self.module_reload_auto_filler.start()

    @tasks.loop(minutes=4, seconds=30)
    async def module_reload_auto_filler(self):
        await self.module_reload_list_updater()

    @commands.group()
    async def modulereload(self, ctx):
        if ctx.author.id != self.bot.authorid:
            raise CommandNotFound

    async def module_reload_list_updater(self):
        now = datetime.now()
        ago = now - timedelta(minutes=5)
        for root, dirs, files in os.walk('cogs/'):
            for fname in files:
                path = os.path.join(root, fname)
                st = os.stat(path)

                if '__pycache__' in str(path) or 'logs' in str(path):
                    continue

                mtime = datetime.fromtimestamp(st.st_mtime)
                module_name = path[:-3].replace('/', '.')
                if mtime > ago and module_name not in self.changed_modules:
                    self.changed_modules.append(module_name)

    @modulereload.command()
    async def reload(self, ctx):
        if ctx.author.id != self.bot.authorid:
            raise CommandNotFound

        for module in self.changed_modules:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
            self.changed_modules.remove(module)

        await ctx.send('Reload was successfully')

    @modulereload.command()
    async def list(self, ctx):
        if ctx.author.id != self.bot.authorid:
            raise CommandNotFound

        return await ctx.send(embed=nextcord.Embed(
            title='List of all Modules that received a change since the last Reload',
            description='\n'.join(self.changed_modules) if self.changed_modules else 'Its empty, no reload needed!',
            color=self.bot.embed_st,
            timestamp=self.bot.current_timestamp))


def setup(bot):
    bot.add_cog(AutoModuleReloader(bot))

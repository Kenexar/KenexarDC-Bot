import os
from datetime import datetime
from datetime import timedelta

from nextcord.ext import commands
from nextcord.ext.commands import CommandNotFound


class AutoModuleReloader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.changed_modules = []

    @commands.Command
    async def modulereload(self, ctx):
        if ctx.author.id != self.bot.authorid:
            raise CommandNotFound

        now = datetime.now()
        ago = now - timedelta(minutes=30)

        for root, dirs, files in os.walk('cogs/'):
            for fname in files:
                path = os.path.join(root, fname)
                st = os.stat(path)

                if '__pycache__' in str(path) or 'logs' in str(path):
                    continue
                mtime = datetime.fromtimestamp(st.st_mtime)
                if mtime > ago:
                    print(f'{path} modified: {mtime}')


def setup(bot):
    bot.add_cog(AutoModuleReloader(bot))

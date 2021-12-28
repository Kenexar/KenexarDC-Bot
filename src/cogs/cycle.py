import platform
from itertools import cycle

import nextcord
from nextcord.ext import commands, tasks

from src.cogs.etc.config import dbBase, PROJECT_NAME
from src.cogs.etc.config import fetch_whitelist
from src.cogs.etc.config import status_query
from src.cogs.etc.embeds import help_site
from src.cogs.etc.presets import get_perm


# todo:
#  remove


class Cycle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.whitelist = fetch_whitelist()

        self.status_list = []
        self.status = cycle(status_query(self.status_list))

    @commands.Cog.listener()
    async def on_ready(self):

        if platform.system() == 'Linux':
            await self.status_task.start()

    @tasks.loop(seconds=30)
    async def status_task(self):
        await self.bot.change_presence(status=nextcord.Status.online,
                                       activity=nextcord.Activity(type=nextcord.ActivityType.watching,
                                                                  name=next(self.status)))

    @commands.command()
    async def cadd(self, ctx):
        cur = dbBase.cursor(buffered=True)
        cur.execute('USE dcbots;')

        if get_perm(ctx.message.author.id) < 5:
            return await ctx.send('You are not authorized to add something to the Presence Query')

        to_check = ctx.message.content[5:].strip()

        if not len(to_check) > 50 and not len(to_check) <= 0:
            cur.execute("insert into roll_text (Name, Text) values (%s, %s);",
                        (PROJECT_NAME, to_check))
            dbBase.commit()
            cur.close()

            self.status_list.append(to_check)
            return await ctx.send(f'Added {to_check} to the Presence Query')
        return await ctx.send(embed=help_site('cadd'))


def setup(bot):
    bot.add_cog(Cycle(bot))

import platform
from itertools import cycle

import nextcord
from cogs.etc.embeds import help_site
from cogs.etc.presets import get_perm
from nextcord.ext import commands, tasks


# todo:
#  remove
from nextcord.ext.commands import CommandNotFound


class Cycle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.whitelist = self.bot.fetch_whitelist()

        self.status_list = []
        self.status = cycle(self.bot.status_query(self.status_list))

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
        if ctx.message.author.id != self.bot.authorid:
            raise CommandNotFound

        cur = self.bot.dbBase.cursor(buffered=True)
        cur.execute('USE dcbots;')

        to_check = ctx.message.content[5:].strip()

        if not len(to_check) > 50 and not len(to_check) <= 0:
            cur.execute("insert into roll_text (Name, Text) values (%s, %s);",
                        (self.bot.project_name, to_check))
            self.bot.dbBase.commit()
            cur.close()

            self.status_list.append(to_check)
            return await ctx.send(f'Added {to_check} to the Presence Query')
        return await ctx.send(embed=await help_site('cadd'))


def setup(bot):
    bot.add_cog(Cycle(bot))

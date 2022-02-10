from nextcord.ext import commands
from nextcord.ext.commands import CommandNotFound

from cogs.etc.config import AUTHORID


class Playin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Command
    async def get_guild_emotes(self, ctx):
        if not ctx.author.id == AUTHORID:
            raise CommandNotFound()

        emojis = {}

        with open(f'all_emotes_{ctx.guild.name}', 'w+') as file:
            for i in ctx.guild.emojis:
                emojis[i.name] = f'<:{i.name}:{i.id}>'
            print(f'file created, all_emotes_{ctx.guild.name}')
            file.write(str(emojis))

def setup(bot):
    bot.add_cog(Playin(bot))
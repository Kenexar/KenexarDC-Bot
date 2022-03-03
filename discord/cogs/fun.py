import nextcord
from nextcord.ext import commands
import json
import requests


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Command
    async def opfer(self, ctx):
        await ctx.send(f'Maul {ctx.message.author.mention}')

    @commands.Command  # testing some stuff
    async def bug(self, ctx):
        return await ctx.send(f'There are no Bugs! only features!')


class Lyrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Command
    async def lyrics(self, ctx, artist, *title):
        res = requests.get(f'https://api.lyrics.ovh/v1/{artist}/{" ".join(title)}')
        embed = nextcord.Embed(title=f'{artist} - {" ".join(title)}',
                               description=res.json().get('lyrics'),
                               color=self.bot.embed_st,
                               timestamp=self.bot.current_timestamp())
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
    bot.add_cog(Lyrics(bot))

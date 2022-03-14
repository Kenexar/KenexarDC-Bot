import asyncio

import nextcord
import requests
from nextcord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Command
    async def opfer(self, ctx):
        await ctx.send(f'Maul {ctx.message.author.mention}')

    @commands.Command  # testing some stuff
    async def bug(self, ctx):
        return await ctx.send(f'Es gibt keine Bugs, nur Features')

    @commands.Command  # testing some MORE STUFF
    async def remindmein(self, ctx: commands.Context, counter):
        if not counter.isdigit():
            return await ctx.send('Der angegebene Wert ist keine zahl.')

        if 600 < int(counter) > 0:
            await asyncio.sleep(int(counter))
            return await ctx.send(f'{ctx.message.author.mention} Die Zeit ist abgelaufen!')
        await ctx.send('Die zeit sollte zwischen 1-600 Sec liegen')


class Lyrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Command
    async def lyrics(self, ctx, artist=None, *title):
        if not artist:
            embed = nextcord.Embed(title='Lyrics - Help',
                                   description=f'Bekomme von einen angegebenen Song die Lyrics. \n**Syntax:** $lyrics (Artist name) (Title)\nArtist namen die Leerzeichen enthalten, sollten zusammen geschrieben werden')
            return await ctx.send(embed=embed)

        res = requests.get(f'https://api.lyrics.ovh/v1/{artist}/{" ".join(title)}')
        embed = nextcord.Embed(title=f'{artist} - {" ".join(title)}',
                               description=res.json().get('lyrics'),
                               color=self.bot.embed_st,
                               timestamp=self.bot.current_timestamp())
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
    bot.add_cog(Lyrics(bot))

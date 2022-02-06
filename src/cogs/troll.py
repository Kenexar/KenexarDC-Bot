import asyncio

import nextcord
from nextcord.ext import commands

from cogs.etc.config import PREFIX


class Troll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.state = True

        self.option = {1: {'path': 'cogs/etc/sounds/Monkie.wav', 'time': 1},
                       2: {'path': 'cogs/etc/sounds/two, four.mp3', 'time': 4},
                       3: {'path': 'cogs/etc/sounds/zone.wav', 'time': 19}}

    @commands.command(aliases=['Monkie', 'zone', 'oneTwo'])
    async def sound(self, ctx):
        channel = ctx.author.voice.channel
        command = ctx.message.content[ctx.message.content.index(PREFIX) + 1:]

        option = {
            'zone': 3,
            'Monkie': 1,
            'oneTwo': 2
        }

        await channel.connect()

        guild = ctx.guild
        voice_client = nextcord.utils.get(self.bot.voice_clients, guild=guild)

        audio_source = nextcord.FFmpegPCMAudio(self.option[option[command]]['path'])
        time_ = self.option[option[command]]['time']

        if not voice_client.is_playing():
            voice_client.play(audio_source, after=None)
            await asyncio.sleep(time_)
            try:
                await ctx.voice_client.disconnect()
            except Exception:
                pass

    @commands.Command
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()


def setup(bot):
    bot.add_cog(Troll(bot))

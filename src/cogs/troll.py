import time
import asyncio

import nextcord
from nextcord.ext import commands


class Troll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.state = True

        self.option = {1: {'path': 'cogs/etc/sounds/Monkie.wav', 'time': 1},
                  2: {'path': 'cogs/etc/sounds/two, four.mp3', 'time': 4}}

    @commands.Command
    async def monkie(self, ctx):
        channel = ctx.author.voice.channel
        await channel.connect()

        guild = ctx.guild
        voice_client = nextcord.utils.get(self.bot.voice_clients, guild=guild)

        # choice = random.randint(0)
        # print(choice)
        if True:
            audio_source = nextcord.FFmpegPCMAudio(self.option[1]['path'])
            time_ = self.option[1]['time']

        # else:
        #     audio_source = nextcord.FFmpegPCMAudio(option[2]['path'])
        #     time_ = option[2]['time']

        if not voice_client.is_playing():
            voice_client.play(audio_source, after=None)
            time.sleep(time_)
            await ctx.voice_client.disconnect()

    @commands.Command
    async def zone(self, ctx):
        channel = ctx.author.voice.channel
        await channel.connect()

        guild = ctx.guild
        voice_client = nextcord.utils.get(self.bot.voice_clients, guild=guild)

        # choice = random.randint(0)
        # print(choice)
        if True:
            audio_source = nextcord.FFmpegPCMAudio(self.option[2]['path'])
            time_ = self.option[2]['time']

        # else:
        #     audio_source = nextcord.FFmpegPCMAudio(option[2]['path'])
        #     time_ = option[2]['time']

        if not voice_client.is_playing():
            voice_client.play(audio_source, after=None)
            time.sleep(time_)
            await ctx.voice_client.disconnect()


    @commands.Command
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()


def setup(bot):
    bot.add_cog(Troll(bot))

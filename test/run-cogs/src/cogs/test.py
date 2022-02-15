import aiohttp

from nextcord import Webhook
import nextcord
from nextcord.ext import commands
from nextcord.ui import View

from flask import Flask, request, abort

from cogs.etc import config

from pydispatch import dispatcher


def event_handler(self, sender):
    print('signal sender', sender)


dispatcher.connect(event_handler, signal='signal', sender=dispatcher.Any)


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('ready')
        # dispatcher.send(signal='moo', sender='me')


    @commands.Command
    async def get_avatar(self, ctx: commands.Context, member: nextcord.Member):
        print(member.avatar.url)

def setup(bot):
    bot.add_cog(Test(bot))

from nextcord.ext import commands as dcommands

from twitchio.ext import commands as tcommands


class TwitchIntegration(dcommands.Cog):
    def __init__(self, bot, **kwargs):
        self.bot = bot

        self.twitch = kwargs.get('twitch')


class DiscordIntegration(tcommands.Cog):
    def __init__(self, bot, **kwargs):
        self.bot = bot

        self.discord = kwargs.get('discord')


def startup(bot):
    bot.add_cog(TwitchIntegration(bot))


def prepare(bot):
    bot.add_cog(DiscordIntegration(bot))

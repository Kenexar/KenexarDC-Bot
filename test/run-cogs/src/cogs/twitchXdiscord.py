from nextcord.ext import commands as dcommands

from twitchio.ext import commands as tcommands

from pydispatch import dispatcher


def handle_event(sender):
    print('Signal from ', sender)


# dispatcher.connect(handle_event, signal='msg.send::discord', sender=dispatcher.Any)


class TwitchIntegration(dcommands.Cog):  # For discord
    def __init__(self, bot, **kwargs):
        self.bot = bot

        self.twitch = kwargs.get('twitch')

        # self.disp = dispatcher.connect(handle_event, signal='msg.send::discord', sender=dispatcher.Any)

    @dcommands.Cog.listener()
    async def on_ready(self):
        print('Discord bot started')
        dispatcher.send(signal='msg.send::discord', sender='discord')


class DiscordIntegration(tcommands.Cog):  # For twitch
    def __init__(self, bot, **kwargs):
        self.bot = bot

        self.discord = kwargs.get('discord')

        self.disp = dispatcher.connect(handle_event, signal='msg.send::discord', sender=dispatcher.Any)

    @tcommands.Cog.event()
    async def event_ready(self):
        print('Twitch bot started')
        dispatcher.send(signal='msg.send::discord', sender='twitch')


def prepare(bot):
    print('twitch')
    bot.add_cog(DiscordIntegration(bot))


# def setup(bot):
#     bot.add_cog(TwitchIntegration(bot))



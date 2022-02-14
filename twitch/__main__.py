from twitchio.ext import commands
from cogs.etc import config

# event_usernotice_subscription(payload)


bot = commands.Bot(token=config.OAUTH,
                   nick=config.BOT_USERNAME,
                   prefix=config.PREFIX,
                   initial_channels=config.CHANNEL_NAME)

if __name__ == '__main__':
    bot.run()

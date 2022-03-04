import json
from datetime import datetime

import nextcord
import requests
from nextcord.ext import commands
from nextcord.ext import tasks


class twitchNotfiy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.config = None
        self.streamer = {}
        self.current = {}

        self.helix_header = {}

    @commands.Cog.listener()
    async def on_ready(self):
        with open('twitchconfig.json', 'r') as c:
            self.config = json.load(c)

        self.helix_header = {
            'Authorization': f'Bearer {self.config.get("OAUTH")}',
            'Client-Id': self.config.get('CLIENT_ID')
        }
        # live = await self.__get_notify()
        # await self.twitch_notify.start(

        await self.twitch_notify.start()

    @tasks.loop(seconds=90)
    async def twitch_notify(self):
        channels = [797891537219747842, 942117088267489340, 942117476991389756]
        # channels = [922920292211392572, 910950168537485332]  # test channel

        live = await self.__get_notify()

        for streamer in live:
            for channel in channels:
                ch = self.bot.get_channel(channel)
                embed = nextcord.Embed(title=f'{streamer.get("user_name")} jetzt Live!',
                                       description=f'**[{streamer.get("title")}](https://twitch.tv/{streamer.get("user_name")})**',
                                       color=0x9146FF,
                                       timestamp=self.bot.current_timestamp())

                embed.add_field(
                    name=f'Spiel: {streamer.get("game_name")} <--> Follower: {await self.__get_follower(streamer.get("user_id"))}',
                    value=f'[Watch Stream](https://twitch.tv/{streamer.get("user_login")})')

                embed.set_image(url=streamer.get('thumbnail_url').format(width='1920', height='1080'))
                embed.set_footer(text='MrPython')

                await ch.send(f'Coinflip Content für @everyone :^)', embed=embed)

    async def __get_app_access_token(self):
        """ PRIVATE - Gets a new OAUTH token when the other is running out

        :return:
        :rtype:
        """
        params = {
            "client_id": self.config.get('CLIENT_ID'),
            "client_secret": self.config.get('CLIENT_SECRET'),
            "grant_type": "client_credentials"
        }

        res = requests.post('https://id.twitch.tv/oauth2/token', params=params)
        access_token = res.json()
        return access_token['access_token']

    async def __get_user(self, user):
        params = {
            "login": user,
        }

        res = requests.get('https://api.twitch.tv/helix/users', params=params, headers=self.helix_header)

        if '<Response [401]>' in str(res):
            self.config['OAUTH'] = await self.__get_app_access_token()
            with open('twitchconfig.json', 'w') as config:
                json.dump(self.config, config)
            with open('twitchconfig.json', 'r') as c:
                self.config = json.load(c)
            return

        return {entry['login']: entry['id'] for entry in res.json()['data']}

    async def __get_streams(self, user: dict):
        params = {
            'user_id': user.values()
        }

        res = requests.get('https://api.twitch.tv/helix/streams', params=params, headers=self.helix_header)
        return {entry['user_login']: entry for entry in res.json()['data']}

    async def __get_notify(self):
        user = await self.__get_user(self.config.get('CHANNEL_NAME'))
        streams = await self.__get_streams(user)

        notify = []
        for user_name in self.config.get('CHANNEL_NAME'):
            if user_name not in self.streamer:
                self.streamer[user_name] = datetime.utcnow()

            if user_name not in streams:
                self.streamer[user_name] = None
            else:
                started_at = datetime.strptime(streams[user_name]['started_at'], "%Y-%m-%dT%H:%M:%SZ")
                if self.streamer[user_name] is None or started_at > self.streamer[user_name]:
                    notify.append(streams[user_name])
                    self.streamer[user_name] = started_at

        return notify

    async def __get_follower(self, streamer_id):
        params = {
            'to_id': streamer_id
        }
        res = requests.get('https://api.twitch.tv/helix/users/follows', params=params, headers=self.helix_header)
        return res.json()['total']


def setup(bot):
    bot.add_cog(twitchNotfiy(bot))

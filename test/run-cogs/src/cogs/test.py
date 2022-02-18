import json
from datetime import datetime

import nextcord
import requests
from nextcord.ext import commands
from nextcord.ext import tasks

testingServer = 762815486823891014


# {'id': '45567579837', 'user_id': '38746172', 'user_login': 'esfandtv', 'user_name': 'EsfandTV', 'game_id': '32982', 'game_name': 'Grand Theft Auto V', 'type': 'live', 'title': '[OTK] CLETUS CORNWOOD 1 MILLION FOLLOWER SUBATHON - !EXTENSION DOWNLOAD IT', 'viewer_count': 6269, 'started_at': '2022-02-18T06:26:34Z', 'language': 'en', 'thumbnail_url': 'https://static-cdn.jtvnw.net/previews-ttv/live_user_esfandtv-{width}x{height}.jpg', 'tag_ids': ['1942f267-26a3-4ee8-9aa0-48cc4aea988e', '6606e54c-f92d-40f6-8257-74977889ccdd', '6ea6bca4-4712-4ab9-a906-e3336a9d8039', '2193eee1-b8f0-43bd-a6d9-dba8a67528a1'], 'is_mature': False}

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.config = None
        self.streamer = {}
        self.current = {}

        self.helix_header = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print('ready g')

        with open('twitchconfig.json', 'r') as c:
            self.config = json.load(c)

        self.helix_header = {
            'Authorization': f'Bearer {self.config.get("OAUTH")}',
            'Client-Id': self.config.get('CLIENT_ID')
        }
        live = await self.__get_notify()
        # await self.twitch_notify.start()
        print('debug')

        ch = self.bot.get_channel(910950168537485332)
        print('debug', live)
        for streamer in live:
            print(ch)
            embed = nextcord.Embed(title=f'{streamer.get("user_name")} jetzt Live!',
                                   description=f'[{streamer.get("title")}](https://twitch.tv/{streamer.get("user_name")})',
                                   color=0x9146FF,
                                   timestamp=self.bot.current_timestamp)
            await ch.send(embed=embed)

    @tasks.loop(minutes=2, seconds=30)
    async def twitch_notify(self):
        channels = [797891537219747842, 942117088267489340, 942117476991389756]
        user = await self.__get_user(self.config.get('CHANNEL_NAME'))
        online_streamer: dict = await self.__get_streams(user)

        for channel in channels:
            channel = self.bot.get_channel(channel)
            for name, data in online_streamer.items():
                pass

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
        current_streams = await self.__get_streams(user)
        notify = []
        for user_name in self.config.get('CHANNEL_NAME'):
            if user_name not in self.streamer:
                self.streamer[user_name] = datetime.utcnow()
            print(user_name)

            if user_name not in current_streams:
                self.streamer[user_name] = None
            else:
                started_at = datetime.strptime(current_streams[user_name]['started_at'], '%Y-%m-%dT%H:%M:%SZ')
                if self.streamer[user_name] is None or started_at > self.streamer[user_name]:
                    notify.append(current_streams[user_name])
                    self.streamer[user_name] = started_at

        return notify


def setup(bot):
    bot.add_cog(Test(bot))

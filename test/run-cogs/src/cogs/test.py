import json


import requests
from nextcord.ext import commands
from nextcord.ext import tasks

testingServer = 762815486823891014


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.config = None

        self.helix_header = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print('ready')

        with open('twitchconfig.json', 'r') as c:
            self.config = json.load(c)

        self.helix_header = {
            'Authorization': f'Bearer {self.config.get("OAUTH")}',
            'Client-Id': self.config.get('CLIENT_ID')
        }

        await self.twitch_notify.start()

    @tasks.loop(minutes=2, seconds=30)
    async def twitch_notify(self):
        print(await self.__get_streams(await self.__get_user()))

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

    async def __get_user(self):
        params = {
            "login": self.config.get('CHANNEL_NAME'),
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


def setup(bot):
    bot.add_cog(Test(bot))

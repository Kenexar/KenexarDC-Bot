import requests

from cogs.etc import config


def get_new_access_token():
    params = {'client_id': config.CLIENT_ID,
              'client_secret': config.CLIENT_SEC,
              'grant_type': 'client_credentials'}

    res = requests.post('https://id.twitch.tv/oauth2/token', params=params)
    token = res.json()['access_token']
    print(token)
    return str('oauth:' + token)


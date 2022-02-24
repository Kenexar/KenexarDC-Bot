from __future__ import annotations

from typing import NewType

import requests

JsonDict = NewType('JsonDict', dict)

all_requests = [
    'get_players',
    'get_player_stats'
]

__all__ = [
    'FaceitAPI',
]


class FaceitAPI:
    """ This is the Client FaceitAPI version for the MrPython """
    __version__ = '1.0.0'

    def __init__(self, api_key):
        self.api_key = api_key

        self.global_headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

    async def get_players(self, player_name: str) -> JsonDict | int:
        """ Get the data for the Giving player

        :param player_name: Give a player name, is it invalid then it returns an error code
        :type player_name: str
        :return: Dictionary with the data or a Http error int
        :rtype: Dict | Int
        """
        res = requests.get(f'https://open.faceit.com/data/v4/players?nickname={player_name}',
                           headers=self.global_headers)

        if res.status_code != 200:
            return res.status_code
        return JsonDict(res.json())

    async def get_player_stats(self, player_id, game='csgo') -> JsonDict | int:
        """ Get the player stats from a Game, standart is CsGO

        :param player_id: The id from the Faceit profile, can getted from get_player["player_id"]
        :type player_id: str
        :param game: Give a game for the Query, standart is CsGO
        :type game: str
        :return: Dictionary | Http error Code
        :rtype: Dict | int
        """
        res = requests.get(f'https://open.faceit.com/data/v4/players/{player_id}/stats/{game}',
                           headers=self.global_headers)

        if res.status_code != 200:
            return res.status_code

        ret = {}
        for key, value in res.json()['lifetime'].items():
            if key == 'Recent Results':
                continue

            ret[key] = value
        return JsonDict(ret)

    def __repr__(self):
        return f'{__name__} > {all_requests}'


if __name__ == '__main__':
    pass

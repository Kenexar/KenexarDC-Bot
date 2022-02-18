# import socket
#
# HOST = '127.0.0.1'
# PORT = 5555
#
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
#     sock.connect((HOST, PORT))
#     sock.sendall(b'Hello, here am I')
#     data = sock.recv(1024)
#
# print('Received: ', repr(data))


# Streamer list => ['user_id']
# if streamer_id in streamer_list: ret
# streamer_list.append(streamer_id)
#
# print('12345' in streamer_list.values())
from pprint import pprint

import requests, json


with open('twitchconfig.json', 'r') as c:
    config = json.load(c)

helix_header = {
    'Authorization': f'Bearer {config.get("OAUTH")}',
    'Client-Id': config.get('CLIENT_ID')
}

b = 515630718


def __get_follower(streamer_id):
    params = {
        'to_id': streamer_id
    }
    res = requests.get('https://api.twitch.tv/helix/users/follows', params=params, headers=helix_header)
    return res.json()['total']


def __get_user(user):
    params = {
        "login": user,
    }

    res = requests.get('https://api.twitch.tv/helix/users', params=params, headers=helix_header)

    return res.json()


if __name__ == '__main__':
    pprint(__get_follower(b))

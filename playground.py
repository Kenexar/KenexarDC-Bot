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


streamer_list = []


def list_filler(user: dict):
    for channel in user:
        if channel['user_id'] in streamer_list:
            return

        streamer_list.append(channel['user_id'])

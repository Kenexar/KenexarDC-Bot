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

from datetime import datetime
import pytz

print(datetime.now(pytz.timezone('Europe/')))

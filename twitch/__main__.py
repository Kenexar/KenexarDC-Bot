import ssl

# from etc import config
import socket


def send(irc: ssl.SSLSocket, message):
    irc.send(bytes(f'{message}\r\n', 'UTF-8'))


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    irc = ctx.wrap_socket(sock)

    irc.connect(('irc.chat.twitch.tv', 6697))

    print(config.OAUTH)
    send(irc, f'PASS {config.OAUTH}')
    send(irc, f'NICK {config.BOT_USERNAME}')
    send(irc, f'JOIN #betrayedxy')

    while True:
        data = irc.recv(1024)
        raw_msg = data.decode('UTF-8')

        for line in raw_msg.splitlines():
            print(line)


if __name__ == '__main__':
    main()

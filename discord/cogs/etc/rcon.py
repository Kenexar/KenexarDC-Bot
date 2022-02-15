import socket


class Rcon:
    """ Rcon Module, interact with the citizen-fx server"""

    def __init__(self, ip, password, port=30120):
        self.ip = ip
        self.port = port
        self.password = password
        self.prefix = bytes([0xff, 0xff, 0xff, 0xff]) + b'rcon '
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_command(self, command, response=True):
        """ Sending commands to server

        :param command: Enter a command that should sent to the server
        :param response: Standart True, turn it to False when you dont want a response
        from the server

        """

        cmd = f"{self.password} {command}".encode()
        query = self.prefix + cmd

        self.socket.connect((self.ip, self.port))
        self.socket.send(query)

        if response:
            self.socket.settimeout(3)
            try:
                data = self.socket.recv(65565)
                return data if data else 'no answer'
            except socket.timeout:
                return 'no answer'

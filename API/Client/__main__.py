import requests
import mysql.connector


class ClientApiKen:
    def __init__(self, auth_token, db):
        self.__authtoken = auth_token
        self.db = db

    async def test(self):
        pass
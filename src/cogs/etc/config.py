import mysql.connector
import os
## [SQL SHIT] ##


def env(value):
  return os.getenv(value)

HOST = env('host')
PASSWORD = env('psw')
DB = 'dcbots'
USER = 'root'

TOKEN = env('TOKEN')
PREFIX = '$'
ESCAPE = '-'
FLASK = True

EMBED_ST = 0xfff
EMBED_RED = 0xff0000
EMBED_GREEN = 0x00ff00

PROJECT_NAME = 'SunSideAdmin'

dbBase = 'USE dcbots;'
DBESSENT = 'USE esx;'

db = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DB
)

CUR = db.cursor(buffered=True)

## [BOT SHIT] ##

config_shit = []
whitelist = []
foo = 1
cur = CUR

CUR.execute(f"SELECT * FROM tokens WHERE Name=%s", (PROJECT_NAME, ))
fetcher = CUR.fetchone()

for _ in range(2):
    foo += 1
    config_shit.append(fetcher[foo])

CUR.execute(f"SELECT * FROM whitelist WHERE Name=%s", (PROJECT_NAME, ))
fetcher = CUR.fetchone()

for i in fetcher:
	whitelist.append(i)

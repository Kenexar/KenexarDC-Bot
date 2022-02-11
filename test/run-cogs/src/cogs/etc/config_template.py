import pytz
from datetime import datetime

import mysql.connector

AUTHORID = 123123123  # Discord id


## [SQL STUFF] ##

HOST = 'YOUR HOST IP' # usally to test something, you use the 127.0.0.1 or localhost
PASSWORD = 'YOUR DB PASSWORD'

DBBASE = 'USE dcbots;'
USER = 'root'

dbBase = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database='DATABASE NAME'
)

cur_db = dbBase.cursor(buffered=True)
cur_db.execute(DBBASE)

## [COLORES] ##
EMBED_ST = 0xffffff
COLOR_RED = 0xff0000
COLOR_GREEN = 0x00ff00
PROJECT_NAME = 'KenexarBot'

config = []
foo = 1


cur_db.execute("SELECT * FROM tokens WHERE Name=%s;", (PROJECT_NAME,))
config.append(cur_db.fetchall()[::])

## [BASE BOT] ##

TOKEN = config[0]
PREFIX = config[3]
current_timestamp = datetime.now(tz=pytz.timezone('Europe/Berlin'))

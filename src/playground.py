from cogs.etc.config import cur_db, dbBase
from cogs.etc.config import DBTEST


# cur_db.execute(DBTEST)
cur_db.execute("SHOW TABLES;")

fetcher = cur_db.fetchall()
print(fetcher, 'f')
cur_db.close()

cur_db = dbBase.cursor()
cur_db.execute("SHOW TABLES;")
print(cur_db.fetchone())

from cogs.etc.config import cur
from cogs.etc.config import DBTEST


cur.execute(DBTEST)
cur.execute("SHOW TABLES;")

fetcher = cur.fetchall()
print(fetcher)



for i in fetcher:
	print(i[0])
	cur.execute(f"SHOW COLUMNS FROM {i[0]};")
	print(cur.fetchall()[:2], '\n')

from cogs.etc.config import cur

cur.execute("SELECT identifier FROM users WHERE identifier='cvoggers'")
if not cur.fetchone():
	print('cpggers')
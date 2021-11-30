from cogs.etc.config import cur

cur.execute("SELECT * FROM trunk_inventory;")
print(cur.fetchone())
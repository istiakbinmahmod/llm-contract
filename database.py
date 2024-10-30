import sqlite3

conn = sqlite3.connect('chemistry.db')

c = conn.cursor()

# c.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
c.execute("SELECT count(*) FROM PostTypes;")

print(c.fetchall())

conn.commit()

conn.close()
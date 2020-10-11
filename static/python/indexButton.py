import sqlite3
import random

conn = sqlite3.connect('randomstock.db')
db = conn.cursor()

# random number generation
stock = random.randint(1, 15031)





# extract stock information
db.execute("SELECT exchange FROM securities WHERE id = ?", (stock,) )
exchange = db.fetchone()
db.execute("SELECT symbol FROM securities WHERE id = ?", (stock,))
symbol = db.fetchone()
db.execute("SELECT name FROM securities WHERE id = ?", (stock,))
stock = db.fetchone()


symbol = symbol[0]
stock = stock[0]
exchange = exchange[0]


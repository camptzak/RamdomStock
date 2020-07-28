from flask import Flask, render_template, request, url_for, redirect, session
from flask_session import Session
import sqlite3
import random

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():

    conn = sqlite3.connect('unplannedInvestments.db')
    db = conn.cursor()

    #random number generation
    NYSE = (random.randint(1, 3298),)
    other = (random.randint(1, 5199),)
    coinFlip = random.randint(0, 1)
    quote = random.randint(0,10)

    #extract random stock from database for NYSE
    db.execute("SELECT symbol FROM NYSE WHERE id = ?", NYSE)
    nyseSymbol = db.fetchone()
    db.execute("SELECT name FROM NYSE WHERE id = ?", NYSE)
    nyseStock = db.fetchone()

    #extract random stock from database for other markets
    db.execute("SELECT symbol FROM other WHERE id = ?", other)
    otherSymbol = db.fetchone()
    db.execute("SELECT name FROM other WHERE id = ?", other)
    otherStock = db.fetchone()




    if (coinFlip == 0):
        symbol = str(nyseSymbol).replace("(", "").replace(")", "").replace(",", "").strip("''")
        stock = str(nyseStock).replace("(", "").replace(")", "").replace(",", "").strip("''")
        return render_template("index.html", symbol=symbol, stock=stock)

    else:
        symbol = (str(otherSymbol)).replace("(", "").replace(")", "").replace(",", "").strip("''")
        stock = (str(otherStock)).replace("(", "").replace(")", "").replace(",", "").strip("''")
        return render_template("index.html", symbol=symbol, stock=stock)

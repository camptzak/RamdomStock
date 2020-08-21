from flask import Flask, render_template, request, url_for, redirect, session, jsonify
from flask_session import Session
import sqlite3
import random
from flask_bootstrap import Bootstrap


application = app = Flask(__name__)


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
    quote = (random.randint(1,33),)

    #extract quote
    db.execute("SELECT quote FROM quotes WHERE id = ?", quote)
    stockquote = db.fetchone()
    db.execute("SELECT author FROM quotes WHERE id = ?", quote)
    quoteauthor = db.fetchone()

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
        stockquotefinal = str(stockquote).replace("(", "").replace(")", "").rstrip(",").strip("''").strip('""')
        quoteauthorfinal = str(quoteauthor).replace("(", "").replace(")", "").replace(",", "").strip("''")
        exchange = 'NYSE'
        return render_template("index.html", symbol=symbol, stock=stock, exchange = exchange, stockquotefinal=stockquotefinal, quoteauthorfinal=quoteauthorfinal)

    else:
        symbol = (str(otherSymbol)).replace("(", "").replace(")", "").replace(",", "").strip("''")
        stock = (str(otherStock)).replace("(", "").replace(")", "").replace(",", "").strip("''")
        stockquotefinal = str(stockquote).replace("(", "").replace(")", "").rstrip(",").strip("''").strip('""')
        quoteauthorfinal = str(quoteauthor).replace("(", "").replace(")", "").replace(",", "").strip("''")
        exchange = 'NASDAQ'
        return render_template("index.html", symbol=symbol, stock=stock, exchange=exchange, stockquotefinal=stockquotefinal, quoteauthorfinal=quoteauthorfinal)


@app.route("/PennyStocks")
def pennyStocks():

    conn = sqlite3.connect('unplannedInvestments.db')
    db = conn.cursor()

    # random number generation
    pennyStock = (random.randint(1, 12018),)
    quote = (random.randint(1, 33),)

    # extract quote
    db.execute("SELECT quote FROM quotes WHERE id = ?", quote)
    stockquote = db.fetchone()
    db.execute("SELECT author FROM quotes WHERE id = ?", quote)
    quoteauthor = db.fetchone()


    # extract random stock from pennyStock database
    db.execute("SELECT symbol FROM pennyStocks WHERE id = ?", pennyStock)
    pennySymbol = db.fetchone()
    db.execute("SELECT name FROM pennyStocks WHERE id = ?", pennyStock)
    pennyName = db.fetchone()
    db.execute("SELECT tier FROM pennyStocks WHERE id = ?", pennyStock)
    pennyMarket = db.fetchone()

    symbolfinal = (str(pennySymbol)).replace("(", "").replace(")", "").replace(",", "").strip("''")
    namefinal = (str(pennyName)).replace("(", "").replace(")", "").replace(",", "").strip("''")
    marketfinal = (str(pennyMarket)).replace("(", "").replace(")", "").replace(",", "").strip("''")
    stockquotefinal = str(stockquote).replace("(", "").replace(")", "").rstrip(",").strip("''").strip('""')
    quoteauthorfinal = str(quoteauthor).replace("(", "").replace(")", "").replace(",", "").strip("''")
    exchange = 'NASDAQ'
    return render_template("pennyStocks.html", symbol=symbolfinal, stock=namefinal, exchange=marketfinal, stockquotefinal=stockquotefinal,
                           quoteauthorfinal=quoteauthorfinal)


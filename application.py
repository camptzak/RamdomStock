from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_session import Session
import sqlite3
import random
from werkzeug.security import check_password_hash, generate_password_hash
from flask_bootstrap import Bootstrap


application = app = Flask(__name__)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():

    conn = sqlite3.connect('unplannedInvestments.db')
    db = conn.cursor()

    # random number generation
    NYSE = (random.randint(1, 3298),)
    other = (random.randint(1, 5199),)
    coinFlip = random.randint(0, 1)
    quote = (random.randint(1,33),)

    # extract quote
    db.execute("SELECT quote FROM quotes WHERE id = ?", quote)
    stockquote = db.fetchone()
    db.execute("SELECT author FROM quotes WHERE id = ?", quote)
    quoteauthor = db.fetchone()


    if (coinFlip == 0):
        # extract random stock from database for NYSE
        db.execute("SELECT symbol FROM NYSE WHERE id = ?", NYSE)
        nyseSymbol = db.fetchone()
        db.execute("SELECT name FROM NYSE WHERE id = ?", NYSE)
        nyseStock = db.fetchone()

        symbol = nyseSymbol[0]
        stock = nyseStock[0]
        stockquotefinal = stockquote[0]
        quoteauthorfinal = quoteauthor[0]
        exchange = 'NYSE'
        return render_template("index.html", symbol=symbol, stock=stock, exchange = exchange, stockquotefinal=stockquotefinal, quoteauthorfinal=quoteauthorfinal)

    else:
        # extract random stock from database for other markets
        db.execute("SELECT symbol FROM other WHERE id = ?", other)
        otherSymbol = db.fetchone()
        db.execute("SELECT name FROM other WHERE id = ?", other)
        otherStock = db.fetchone()


        symbol = otherSymbol[0]
        stock = otherStock[0]
        stockquotefinal = stockquote[0]
        quoteauthorfinal = quoteauthor[0]
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

    symbolfinal = pennySymbol[0]
    namefinal = pennyName[0]
    marketfinal = pennyMarket[0]
    stockquotefinal = stockquote[0]
    quoteauthorfinal = quoteauthor[0]
    return render_template("pennyStocks.html", symbol=symbolfinal, stock=namefinal, exchange=marketfinal, stockquotefinal=stockquotefinal,
                           quoteauthorfinal=quoteauthorfinal)

@app.route("/crypto")
def crypto():

    conn = sqlite3.connect('unplannedInvestments.db')
    db = conn.cursor()

    # random number generation
    crypto = (random.randint(1, 1754),)
    quote = (random.randint(1, 33),)

    # extract quote
    db.execute("SELECT quote FROM quotes WHERE id = ?", quote)
    stockquote = db.fetchone()
    db.execute("SELECT author FROM quotes WHERE id = ?", quote)
    quoteauthor = db.fetchone()


    # extract random stock from pennyStock database
    db.execute("SELECT symbol FROM crypto WHERE id = ?", crypto)
    cryptoSymbol = db.fetchone()
    db.execute("SELECT name FROM pennyStocks WHERE id = ?", crypto)
    cryptoName = db.fetchone()
    db.execute("SELECT lookup FROM crypto WHERE id = ?", crypto)
    cryptolookup = db.fetchone()
    cryptoMarket = "CoinBase"

    symbolfinal = cryptoSymbol[0]
    namefinal = cryptoName[0]
    marketfinal = cryptoMarket
    lookup = cryptolookup[0]
    stockquotefinal = stockquote[0]
    quoteauthorfinal = quoteauthor[0]
    return render_template("crypto.html", symbol=symbolfinal, stock=namefinal, exchange=marketfinal, lookup = lookup, stockquotefinal=stockquotefinal,
                           quoteauthorfinal=quoteauthorfinal,)

@app.route("/blog/blog")
def blog():
    return render_template("blog.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    conn = sqlite3.connect('unplannedInvestments.db')
    db = conn.cursor()

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            flash("Sorry! You must provide a username", "error")
            redirect(url_for("login"))
            return render_template("login.html")

        # Ensure password was submitted
        elif not password:
            flash("Sorry! You must provide a password", "error")
            redirect(url_for("login"))
            return render_template("login.html")


        # Query database for username
        db.execute("SELECT * FROM users WHERE username = ?", (username,))
        rows = db.fetchone()
        print(rows)

        if not rows:
            flash("Sorry, that username does not exist", "error")
            redirect(url_for("login"))
            return render_template("login.html")

        if not check_password_hash(rows[2], password):
            flash("Sorry, your password is not correct", "error")
            redirect(url_for("login"))
            return render_template("login.html")

        session["user_id"] = rows[0]
        flash("Login Successful", "info")

        # Redirect user to home page
        return redirect(url_for("index"))

    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    conn = sqlite3.connect('unplannedInvestments.db')
    db = conn.cursor()

    # Clear any session data
    session.clear()

    if request.method == "POST":
        username = request.form.get("username_register")
        password = request.form.get("password_register")
        email = request.form.get("email_register")

        if not username or not password or not email:
            flash("Sorry! You must enter a username, password, and email", "error")
            redirect(url_for("register"))
            return render_template("register.html")

        if " " in username:
            flash("Sorry! Your username cannot contain a space", "error")
            redirect(url_for("register"))
            return render_template("register.html")

        if " " in password:
            flash("Sorry! Your password cannot contain a space", "error")
            redirect(url_for("register"))
            return render_template("register.html")

        if " " in email:
            flash("Sorry! Your email cannot contain a space", "error")
            redirect(url_for("register"))
            return render_template("register.html")

        # Check if username exists already
        db.execute("SELECT * FROM users WHERE username = ?", (username,))
        rows = db.fetchone()
        if rows:
            flash("Sorry! That username is already taken", "error")
            redirect(url_for("register"))
            return render_template("register.html")


        hashpassword = generate_password_hash(password)

        db.execute("INSERT INTO users (username, hash, email) VALUES (?, ?, ?)", (username, hashpassword, email,))
        conn.commit()
        flash("Registration Successful!", "info")
        redirect(url_for("login"))
        return render_template("login.html")

    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    flash("Logged out Successfully", "info")
    return redirect(url_for("index"))
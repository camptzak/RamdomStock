from flask import Flask, render_template, request, url_for, redirect, session, flash, jsonify
from flask_session import Session
import sqlite3
import random
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from flask_bootstrap import Bootstrap

application = app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    conn = sqlite3.connect('randomstock.db')
    db = conn.cursor()

    # Uncheck all the boxes in the session dictionary
    session["AMEX"] = False
    session["LSE"] = False
    session["AMEX"] = False
    session["NASDAQ"] = False
    session["NYSE"] = False
    session["SGX"] = False


    # random number generation
    stock = random.randint(1, 15031)
    quote = random.randint(1, 33)

    # extract quote
    db.execute("SELECT quote FROM quotes WHERE id = ?", (quote,))
    stockquote = db.fetchone()
    db.execute("SELECT author FROM quotes WHERE id = ?", (quote,))
    quoteauthor = db.fetchone()

    # extract stock information
    db.execute("SELECT exchange FROM securities WHERE id = ?", (stock,))
    exchange = db.fetchone()
    db.execute("SELECT symbol FROM securities WHERE id = ?", (stock,))
    symbol = db.fetchone()
    db.execute("SELECT name FROM securities WHERE id = ?", (stock,))
    stock = db.fetchone()

    symbol = symbol[0]
    stock = stock[0]
    stockquotefinal = stockquote[0]
    quoteauthorfinal = quoteauthor[0]
    exchange = exchange[0]
    return render_template("index.html", symbol=symbol, stock=stock, exchange=exchange, stockquotefinal=stockquotefinal,
                           quoteauthorfinal=quoteauthorfinal)


@app.route("/_indexButton")
def _indexButton():
    conn = sqlite3.connect('randomstock.db')
    db = conn.cursor()

    stock = random.randint(0, 15031)

    # extract stock information
    db.execute("SELECT exchange FROM securities WHERE id = ?", (stock,))
    exchange = db.fetchone()
    db.execute("SELECT symbol FROM securities WHERE id = ?", (stock,))
    symbol = db.fetchone()
    db.execute("SELECT name FROM securities WHERE id = ?", (stock,))
    stock = db.fetchone()

    symbol = symbol[0]
    company = stock[0]
    exchange = exchange[0]
    return jsonify(symbol=symbol, company=company, exchange=exchange)


@app.route("/PennyStocks")
def pennyStocks():
    conn = sqlite3.connect('randomstock.db')
    db = conn.cursor()

    # random number generation
    stock = random.randint(15032, 25514)
    quote = random.randint(1, 33)

    # extract quote
    db.execute("SELECT quote FROM quotes WHERE id = ?", (quote,))
    stockquote = db.fetchone()
    db.execute("SELECT author FROM quotes WHERE id = ?", (quote,))
    quoteauthor = db.fetchone()

    # extract stock info from OTC section
    db.execute("SELECT symbol FROM securities WHERE id = ?", (stock,))
    symbol = db.fetchone()
    db.execute("SELECT name FROM securities WHERE id = ?", (stock,))
    stock = db.fetchone()

    symbolfinal = symbol[0]
    namefinal = stock[0]
    marketfinal = 'OTCBB'
    stockquotefinal = stockquote[0]
    quoteauthorfinal = quoteauthor[0]
    return render_template("pennyStocks.html", symbol=symbolfinal, stock=namefinal, exchange=marketfinal,
                           stockquotefinal=stockquotefinal,
                           quoteauthorfinal=quoteauthorfinal)


@app.route("/_pennyButton")
def _pennyButton():
    conn = sqlite3.connect('randomstock.db')
    db = conn.cursor()

    # random number generation
    stock = random.randint(15032, 25514)

    # extract stock information
    db.execute("SELECT symbol FROM securities WHERE id = ?", (stock,))
    symbol = db.fetchone()
    db.execute("SELECT name FROM securities WHERE id = ?", (stock,))
    stock = db.fetchone()

    symbol = symbol[0]
    company = stock[0]
    return jsonify(symbol=symbol, company=company)


@app.route("/crypto")
def crypto():
    conn = sqlite3.connect('randomstock.db')
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
    db.execute("SELECT name FROM crypto WHERE id = ?", crypto)
    cryptoName = db.fetchone()
    db.execute("SELECT lookup FROM crypto WHERE id = ?", crypto)
    cryptolookup = db.fetchone()


    symbolfinal = cryptoSymbol[0]
    namefinal = cryptoName[0]
    lookup = cryptolookup[0]
    stockquotefinal = stockquote[0]
    quoteauthorfinal = quoteauthor[0]
    return render_template("crypto.html", symbol=symbolfinal, stock=namefinal, exchange="Coinbase", lookup=lookup,
                           stockquotefinal=stockquotefinal,
                           quoteauthorfinal=quoteauthorfinal, )


@app.route("/_cryptoButton")
def _cryptoButton():
    conn = sqlite3.connect('randomstock.db')
    db = conn.cursor()

    # random number generation
    stock = random.randint(1, 1754)

    # extract stock information
    db.execute("SELECT lookup FROM crypto WHERE id = ?", (stock,))
    cryptolookup = db.fetchone()
    db.execute("SELECT symbol FROM crypto WHERE id = ?", (stock,))
    symbol = db.fetchone()
    db.execute("SELECT name FROM crypto WHERE id = ?", (stock,))
    stock = db.fetchone()

    symbol = symbol[0]
    company = stock[0]
    lookup = cryptolookup[0]
    return jsonify(symbol=symbol, company=company, lookup=lookup)


@app.route("/login", methods=["GET", "POST"])
def login():
    conn = sqlite3.connect('randomstock.db')
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
        session["username"] = rows[1]
        flash("Login Successful", "info")

        # Redirect user to home page
        return redirect(url_for("index"))

    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    conn = sqlite3.connect('randomstock.db')
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


@app.route("/blog")
def blog():
    return render_template("blog/blog.html")


# Blog Posts

@app.route("/ValueInCrypto", methods=["GET", "POST"])
def ValueInCrypto():
    if request.method == "POST":

        if session.get("user_id") is None:
            flash("Sorry! You must be logged in to post a comment", "error")
            return redirect(url_for("ValueInCrypto"))

        comment = request.form["comment"]
        username = session.get("username")
        date = (str(datetime.datetime.now())).split(".")
        date = date[0]

        article = 1

        conn = sqlite3.connect('randomstock.db')
        db = conn.cursor()

        db.execute("INSERT INTO comments (article, comment, user, date) VALUES (?, ?, ?, ?)",
                   (article, comment, username, date))
        conn.commit()

        return redirect(url_for("ValueInCrypto"))

    else:
        conn = sqlite3.connect('randomstock.db')
        db = conn.cursor()
        db.execute("SELECT * FROM comments WHERE article = 1")
        rows = db.fetchall()

    return render_template("blog/ValueInCrypto.html", rows=rows)


@app.route("/coronaVaccine", methods=["GET", "POST"])
def coronaVaccine():
    if request.method == "POST":

        if session.get("user_id") is None:
            flash("Sorry! You must be logged in to post a comment", "error")
            return redirect(url_for("coronaVaccine"))

        comment = request.form["comment"]
        username = session.get("username")
        date = (str(datetime.datetime.now())).split(".")
        date = date[0]

        article = 2

        conn = sqlite3.connect('randomstock.db')
        db = conn.cursor()

        db.execute("INSERT INTO comments (article, comment, user, date) VALUES (?, ?, ?, ?)",
                   (article, comment, username, date))
        conn.commit()

        return redirect(url_for("coronaVaccine"))

    else:
        conn = sqlite3.connect('randomstock.db')
        db = conn.cursor()
        db.execute("SELECT * FROM comments WHERE article = 2")
        rows = db.fetchall()

    return render_template("blog/coronaVaccine.html", rows=rows)

@app.route("/randomness", methods=["GET", "POST"])
def randomness():
    if request.method == "POST":

        if session.get("user_id") is None:
            flash("Sorry! You must be logged in to post a comment", "error")
            return redirect(url_for("randomness"))

        comment = request.form["comment"]
        username = session.get("username")
        date = (str(datetime.datetime.now())).split(".")
        date = date[0]

        article = 3

        conn = sqlite3.connect('randomstock.db')
        db = conn.cursor()

        db.execute("INSERT INTO comments (article, comment, user, date) VALUES (?, ?, ?, ?)",
                   (article, comment, username, date))
        conn.commit()

        return redirect(url_for("randomness"))

    else:
        conn = sqlite3.connect('randomstock.db')
        db = conn.cursor()
        db.execute("SELECT * FROM comments WHERE article = 3")
        rows = db.fetchall()

    return render_template("blog/randomness.html", rows=rows)


@app.route("/TSLAshort", methods=["GET", "POST"])
def TSLAshort():
    if request.method == "POST":

        if session.get("user_id") is None:
            flash("Sorry! You must be logged in to post a comment", "error")
            return redirect(url_for("TSLAshort"))

        comment = request.form["comment"]
        username = session.get("username")
        date = (str(datetime.datetime.now())).split(".")
        date = date[0]

        article = 4

        conn = sqlite3.connect('randomstock.db')
        db = conn.cursor()

        db.execute("INSERT INTO comments (article, comment, user, date) VALUES (?, ?, ?, ?)",
                   (article, comment, username, date))
        conn.commit()

        return redirect(url_for("TSLAshort"))

    else:
        conn = sqlite3.connect('randomstock.db')
        db = conn.cursor()
        db.execute("SELECT * FROM comments WHERE article = 4")
        rows = db.fetchall()

    return render_template("blog/TSLAshort.html", rows=rows)

@app.route("/thirteenf", methods=["GET", "POST"])
def thirteenf():
    if request.method == "POST":

        if session.get("user_id") is None:
            flash("Sorry! You must be logged in to post a comment", "error")
            return redirect(url_for("thirteenf"))

        comment = request.form["comment"]
        username = session.get("username")
        date = (str(datetime.datetime.now())).split(".")
        date = date[0]

        article = 5

        conn = sqlite3.connect('randomstock.db')
        db = conn.cursor()

        db.execute("INSERT INTO comments (article, comment, user, date) VALUES (?, ?, ?, ?)",
                   (article, comment, username, date))
        conn.commit()

        return redirect(url_for("thirteenf"))

    else:
        conn = sqlite3.connect('randomstock.db')
        db = conn.cursor()
        db.execute("SELECT * FROM comments WHERE article = 5")
        rows = db.fetchall()

    return render_template("blog/thirteenf.html", rows=rows)


@app.route("/PDC", methods=["GET", "POST"])
def PDC():
    if request.method == "POST":

        if session.get("user_id") is None:
            flash("Sorry! You must be logged in to post a comment", "error")
            return redirect(url_for("PDC"))

        comment = request.form["comment"]
        username = session.get("username")
        date = (str(datetime.datetime.now())).split(".")
        date = date[0]

        article = 6

        conn = sqlite3.connect('randomstock.db')
        db = conn.cursor()

        db.execute("INSERT INTO comments (article, comment, user, date) VALUES (?, ?, ?, ?)",
                   (article, comment, username, date))
        conn.commit()

        return redirect(url_for("PDC"))

    else:
        conn = sqlite3.connect('randomstock.db')
        db = conn.cursor()
        db.execute("SELECT * FROM comments WHERE article = 6")
        rows = db.fetchall()

    return render_template("blog/PDC.html", rows=rows)
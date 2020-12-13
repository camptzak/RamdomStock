from flask import Flask, render_template, request, url_for, redirect, session, flash, jsonify
from flask_session import Session
import sqlite3
import random
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import pandas as pd
from flask_bootstrap import Bootstrap
import yahoo_fin.stock_info as si

application = app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    conn = sqlite3.connect('randomstock.db')
    db = conn.cursor()

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


@app.route("/_indexButton", methods=["GET", "POST"])
def _indexButton():
    if request.method == "POST":

        AMEX = request.form["AMEX"]
        LSE = request.form["LSE"]
        NASDAQ = request.form["NASDAQ"]
        NYSE = request.form["NYSE"]
        SGX = request.form["SGX"]

        exchanges = []

        if AMEX == 'true':
            amex = random.randint(1, 2248)
            exchanges.append(amex)
        if LSE == 'true':
            lse = random.randint(2249, 7117)
            exchanges.append(lse)
        if NASDAQ == 'true':
            nasdaq = random.randint(7118, 10755)
            exchanges.append(nasdaq)
        if NYSE == 'true':
            nyse = random.randint(10756, 13910)
            exchanges.append(nyse)
        if SGX == 'true':
            sgx = random.randint(13910, 15031)
            exchanges.append(sgx)

        if not exchanges:
            stock = random.randint(1, 15031)

        else:
            lengthOfList = len(exchanges) - 1

            randomNumber = random.randint(0, lengthOfList)

            stock = exchanges[randomNumber]

        conn = sqlite3.connect('randomstock.db')
        db = conn.cursor()

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

    else:
        conn = sqlite3.connect('randomstock.db')
        db = conn.cursor()

        stock = random.randint(1, 15031)

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


@app.route("/analysis", methods=["GET", "POST"])
def analysis():
    if request.method == "POST":

        def isNaN(data):
            return data != data

        def dataCheck(dict, key):
            if key not in dict.keys():
                return 'No Data'

            elif isNaN(quoteTable[key]):
                return 'No Data'

            else:
                return quoteTable[key]

        symbol = request.form["symbolInput"]

        try:
            quoteTable = si.get_quote_table(symbol)

        except (RuntimeError, TypeError, NameError, IndexError, ValueError, KeyError):
            quoteTable = None

        if quoteTable != None:
            # print("QuoteTableExists")

            oneYearTargetEst = dataCheck(quoteTable, '1y Target Est')
            # print(oneYearTargetEst)

            fiftyTwoWeekRange = dataCheck(quoteTable, '52 Week Range')
            # print(fiftyTwoWeekRange)

            ask = dataCheck(quoteTable, 'Ask')
            # print(ask)

            averageVolume = dataCheck(quoteTable, 'Avg. Volume')
            # print(averageVolume)

            beta = dataCheck(quoteTable, 'Beta (5Y Monthly)')
            # print(beta)

            bid = dataCheck(quoteTable, 'Bid')
            # print(bid)

            daysRange = dataCheck(quoteTable, "Day's Range")
            # print(daysRange)

            EPS = dataCheck(quoteTable, 'EPS (TTM)')
            # print(EPS)

            earningsDate = dataCheck(quoteTable, 'Earnings Date')
            # print(earningsDate)

            exDividendDate = dataCheck(quoteTable, 'Ex-Dividend Date')
            # print(exDividendDate)

            forwardDividendAndYield = dataCheck(quoteTable, 'Forward Dividend & Yield')
            # print(forwardDividendAndYield)

            marketCap = dataCheck(quoteTable, 'Market Cap')
            # print(marketCap)

            open = dataCheck(quoteTable, 'Open')
            # print(open)

            peRatio = dataCheck(quoteTable, 'PE Ratio (TTM)')
            # print(peRatio)

            previousClose = dataCheck(quoteTable, 'Previous Close')
            # print(previousClose)

            quotePrice = dataCheck(quoteTable, 'Quote Price')
            quotePrice = round(quotePrice, 4)
            # print(quotePrice)

            volume = dataCheck(quoteTable, 'Volume')
            # print(volume)




            return render_template("analysis.html", symbol=symbol,
                           oneYearTargetEst=oneYearTargetEst,
                           fiftyTwoWeekRange=fiftyTwoWeekRange,
                           ask=ask,
                           averageVolume=averageVolume,
                           beta=beta,
                           bid=bid,
                           daysRange=daysRange,
                           EPS=EPS,
                           earningsDate=earningsDate,
                           exDividendDate=exDividendDate,
                           forwardDividendAndYield=forwardDividendAndYield,
                           marketCap=marketCap,
                           open=open,
                           peRatio=peRatio,
                           previousClose=previousClose,
                           quotePrice=quotePrice,
                           volume=volume)

        else:
            flash("Sorry! We don't have any data for that symbol", "error")
            redirect(url_for("analysis"))
            return render_template("analysis.html")


    else:
        return render_template("analysis.html")


@app.route("/_analysis", methods=["POST"])
def _analysis():

    def isNaN(data):
        return data != data

    def dataCheck(dict, key):
        if key not in dict.keys():
            return 'No Data'

        elif isNaN(quoteTable[key]):
            return 'No Data'

        else:
            return quoteTable[key]



    exchange = request.form["exchange"]
    symbol = request.form["symbol"]
    print(exchange)
    print(symbol)

    try:
        quoteTable = si.get_quote_table(symbol)

    except (RuntimeError, TypeError, NameError, IndexError, ValueError):
        quoteTable = None

    if quoteTable != None:
        print("QuoteTableExists")

        oneYearTargetEst = dataCheck(quoteTable, '1y Target Est')
        print(oneYearTargetEst)

        fiftyTwoWeekRange = dataCheck(quoteTable, '52 Week Range')
        print(fiftyTwoWeekRange)

        ask = dataCheck(quoteTable, 'Ask')
        print(ask)

        averageVolume = dataCheck(quoteTable, 'Avg. Volume')
        print(averageVolume)

        beta = dataCheck(quoteTable, 'Beta (5Y Monthly)')
        print(beta)

        bid = dataCheck(quoteTable, 'Bid')
        print(bid)

        daysRange = dataCheck(quoteTable, "Day's Range")
        print(daysRange)

        EPS = dataCheck(quoteTable, 'EPS (TTM)')
        print(EPS)

        earningsDate = dataCheck(quoteTable, 'Earnings Date')
        print(earningsDate)

        exDividendDate = dataCheck(quoteTable,'Ex-Dividend Date')
        print(exDividendDate)

        forwardDividendAndYield = dataCheck(quoteTable, 'Forward Dividend & Yield')
        print(forwardDividendAndYield)

        marketCap = dataCheck(quoteTable, 'Market Cap')
        print(marketCap)

        open = dataCheck(quoteTable, 'Open')
        print(open)

        peRatio = dataCheck(quoteTable, 'PE Ratio (TTM)')
        print(peRatio)

        previousClose = dataCheck(quoteTable, 'Previous Close')
        print(previousClose)

        quotePrice = dataCheck(quoteTable, 'Quote Price')
        print(quotePrice)

        volume = dataCheck(quoteTable, 'Volume')
        print(volume)


        return jsonify(exchange=exchange, symbol=symbol,
                       oneYearTargetEst=oneYearTargetEst,
                       fiftyTwoWeekRange=fiftyTwoWeekRange,
                       ask=ask,
                       averageVolume=averageVolume,
                       beta=beta,
                       bid=bid,
                       daysRange=daysRange,
                       EPS=EPS,
                       earningsDate=earningsDate,
                       exDividendDate=exDividendDate,
                       forwardDividendAndYield=forwardDividendAndYield,
                       marketCap=marketCap,
                       open=open,
                       peRatio=peRatio,
                       previousClose=previousClose,
                       quotePrice=quotePrice,
                       volume=volume)

    else:
        print('No Quote Table')
        return jsonify(exchange=exchange, symbol=symbol)


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


@app.route("/ExpectedValue", methods=["GET", "POST"])
def ExpectedValue():
    if request.method == "POST":

        if session.get("user_id") is None:
            flash("Sorry! You must be logged in to post a comment", "error")
            return redirect(url_for("ExpectedValue"))

        comment = request.form["comment"]
        username = session.get("username")
        date = (str(datetime.datetime.now())).split(".")
        date = date[0]

        article = 7

        conn = sqlite3.connect('randomstock.db')
        db = conn.cursor()

        db.execute("INSERT INTO comments (article, comment, user, date) VALUES (?, ?, ?, ?)",
                   (article, comment, username, date))
        conn.commit()

        return redirect(url_for("ExpectedValue"))

    else:
        conn = sqlite3.connect('randomstock.db')
        db = conn.cursor()
        db.execute("SELECT * FROM comments WHERE article = 7")
        rows = db.fetchall()

    return render_template("blog/ExpectedValue.html", rows=rows)


@app.route("/Savings", methods=["GET", "POST"])
def Savings():
    if request.method == "POST":

        if session.get("user_id") is None:
            flash("Sorry! You must be logged in to post a comment", "error")
            return redirect(url_for("Savings"))

        comment = request.form["comment"]
        username = session.get("username")
        date = (str(datetime.datetime.now())).split(".")
        date = date[0]

        article = 8

        conn = sqlite3.connect('randomstock.db')
        db = conn.cursor()

        db.execute("INSERT INTO comments (article, comment, user, date) VALUES (?, ?, ?, ?)",
                   (article, comment, username, date))
        conn.commit()

        return redirect(url_for("Savings"))

    else:
        conn = sqlite3.connect('randomstock.db')
        db = conn.cursor()
        db.execute("SELECT * FROM comments WHERE article = 8")
        rows = db.fetchall()

    return render_template("blog/savings.html", rows=rows)


@app.route("/Opportunity", methods=["GET", "POST"])
def Opportunity():
    if request.method == "POST":

        if session.get("user_id") is None:
            flash("Sorry! You must be logged in to post a comment", "error")
            return redirect(url_for("Opportunity"))

        comment = request.form["comment"]
        username = session.get("username")
        date = (str(datetime.datetime.now())).split(".")
        date = date[0]

        article = 9

        conn = sqlite3.connect('randomstock.db')
        db = conn.cursor()

        db.execute("INSERT INTO comments (article, comment, user, date) VALUES (?, ?, ?, ?)",
                   (article, comment, username, date))
        conn.commit()

        return redirect(url_for("Opportunity"))

    else:
        conn = sqlite3.connect('randomstock.db')
        db = conn.cursor()
        db.execute("SELECT * FROM comments WHERE article = 9")
        rows = db.fetchall()

    return render_template("blog/opportunity.html", rows=rows)


@app.route("/DollarCostAveraging", methods=["GET", "POST"])
def DollarCostAveraging():
    if request.method == "POST":

        if session.get("user_id") is None:
            flash("Sorry! You must be logged in to post a comment", "error")
            return redirect(url_for("DollarCostAveraging"))

        comment = request.form["comment"]
        username = session.get("username")
        date = (str(datetime.datetime.now())).split(".")
        date = date[0]

        article = 10

        conn = sqlite3.connect('randomstock.db')
        db = conn.cursor()

        db.execute("INSERT INTO comments (article, comment, user, date) VALUES (?, ?, ?, ?)",
                   (article, comment, username, date))
        conn.commit()

        return redirect(url_for("DollarCostAveraging"))

    else:
        conn = sqlite3.connect('randomstock.db')
        db = conn.cursor()
        db.execute("SELECT * FROM comments WHERE article = 10")
        rows = db.fetchall()

    return render_template("blog/DollarCostAveraging.html", rows=rows)


@app.route("/FiveRulesToInvesting", methods=["GET", "POST"])
def FiveRulesToInvesting():
    if request.method == "POST":

        if session.get("user_id") is None:
            flash("Sorry! You must be logged in to post a comment", "error")
            return redirect(url_for("FiveRulesToInvesting"))

        comment = request.form["comment"]
        username = session.get("username")
        date = (str(datetime.datetime.now())).split(".")
        date = date[0]

        article = 11

        conn = sqlite3.connect('randomstock.db')
        db = conn.cursor()

        db.execute("INSERT INTO comments (article, comment, user, date) VALUES (?, ?, ?, ?)",
                   (article, comment, username, date))
        conn.commit()

        return redirect(url_for("FiveRulesToInvesting"))

    else:
        conn = sqlite3.connect('randomstock.db')
        db = conn.cursor()
        db.execute("SELECT * FROM comments WHERE article = 11")
        rows = db.fetchall()

    return render_template("blog/FiveRulesToInvesting.html", rows=rows)


@app.route("/WhenToSellYourStake", methods=["GET", "POST"])
def WhenToSellYourStake():
    if request.method == "POST":

        if session.get("user_id") is None:
            flash("Sorry! You must be logged in to post a comment", "error")
            return redirect(url_for("WhenToSellYourStake"))

        comment = request.form["comment"]
        username = session.get("username")
        date = (str(datetime.datetime.now())).split(".")
        date = date[0]

        article = 12

        conn = sqlite3.connect('randomstock.db')
        db = conn.cursor()

        db.execute("INSERT INTO comments (article, comment, user, date) VALUES (?, ?, ?, ?)",
                   (article, comment, username, date))
        conn.commit()

        return redirect(url_for("WhenToSellYourStake"))

    else:
        conn = sqlite3.connect('randomstock.db')
        db = conn.cursor()
        db.execute("SELECT * FROM comments WHERE article = 12")
        rows = db.fetchall()

    return render_template("blog/WhenToSellYourStake.html", rows=rows)


@app.route("/InvestingInAStartUp", methods=["GET", "POST"])
def InvestingInAStartUp():
    if request.method == "POST":

        if session.get("user_id") is None:
            flash("Sorry! You must be logged in to post a comment", "error")
            return redirect(url_for("InvestingInAStartUp"))

        comment = request.form["comment"]
        username = session.get("username")
        date = (str(datetime.datetime.now())).split(".")
        date = date[0]

        article = 13

        conn = sqlite3.connect('randomstock.db')
        db = conn.cursor()

        db.execute("INSERT INTO comments (article, comment, user, date) VALUES (?, ?, ?, ?)",
                   (article, comment, username, date))
        conn.commit()

        return redirect(url_for("InvestingInAStartUp"))

    else:
        conn = sqlite3.connect('randomstock.db')
        db = conn.cursor()
        db.execute("SELECT * FROM comments WHERE article = 13")
        rows = db.fetchall()

    return render_template("blog/InvestingInAStartUp.html", rows=rows)

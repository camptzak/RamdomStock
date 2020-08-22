#Random Stock bot
import tweepy as tp
from datetime import date
import random
import sqlite3

# credentials to login to twitter api
consumer_key = "AXHW5hnecwgi6sYrvDiFCzt6U"
consumer_secret = "w0jv8jLZkTWmzy48ibUiILtznwF86eGjuBDKGQUink4Wx7ipm6"
access_token = "1288853810388045826-7GRXj7T045cZA880eVV1pLPHVks8rw"
access_secret = "gTLOnWTlU2fEDUE7HcANRcWUVhxYzfaAjY860nO9tx9Ko"

#login to twitter account api
auth = tp.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tp.API(auth)

# The bot function

listOne = ["Have a Great", "Have a Wonderful", "Happy", "Have a Fantastic"]
randOne = random.randint(0, 3)
greeting = listOne[randOne]

listTwo = ["All", "Everyone", "Everybody Out There", "Everybody"]
randTwo = random.randint(0, 3)
everyone = listTwo[randTwo]

listThree = ["Have a great day!", "Have a wonderful day!", "Have a fantastic day!", "Have an amazing day!", "Have an awesome day!"]
randThree = random.randint(0, 4)
goodbye = listThree[randThree]
today = date.today()

day = date.weekday(today)
if day == 0:
    greetings = "%s Monday %s!" % (greeting, everyone)

if day == 1:
    greetings = "%s Tuesday %s!" % (greeting, everyone)

if day == 2:
    greetings = "%s Wednesday %s!" % (greeting, everyone)

if day == 3:
    greetings = "%s Thursday %s!" % (greeting, everyone)

if day == 4:
    greetings = "%s Friday %s!" % (greeting, everyone)

if day == 5:
    greetings = "%s Saturday %s!" % (greeting, everyone)

if day == 6:
    greetings = "%s Sunday %s!" % (greeting, everyone)

conn = sqlite3.connect('unplannedInvestments.db')
db = conn.cursor()



threeSidedCoinFlip = random.randint(0, 2)


if threeSidedCoinFlip == 0:
    # extract random stock from database for NYSE
    NYSE = (random.randint(1, 3298),)
    db.execute("SELECT symbol FROM NYSE WHERE id = ?", NYSE)
    nyseSymbol = db.fetchone()
    db.execute("SELECT name FROM NYSE WHERE id = ?", NYSE)
    nyseStock = db.fetchone()
    symbol = nyseSymbol[0]
    name = nyseStock[0]
    exchange = 'NYSE'

if threeSidedCoinFlip == 1:
    # extract random stock from database for other markets
    other = (random.randint(1, 5199),)
    db.execute("SELECT symbol FROM other WHERE id = ?", other)
    otherSymbol = db.fetchone()
    db.execute("SELECT name FROM other WHERE id = ?", other)
    otherStock = db.fetchone()
    symbol = otherSymbol[0]
    name = otherStock[0]
    exchange = 'NASDAQ'

# extract random stock from pennyStock database
if threeSidedCoinFlip == 2:
    pennyStock = (random.randint(1, 12018),)
    db.execute("SELECT symbol FROM pennyStocks WHERE id = ?", pennyStock)
    pennySymbol = db.fetchone()
    db.execute("SELECT name FROM pennyStocks WHERE id = ?", pennyStock)
    pennyName = db.fetchone()
    db.execute("SELECT tier FROM pennyStocks WHERE id = ?", pennyStock)
    pennyMarket = db.fetchone()
    symbol = pennySymbol[0]
    name = pennyName[0]
    exchange = pennyMarket[0]


tweet = "%s Todays Random Stock is: \n" \
"Symbol: %s \n" \
"Company: %s \n" \
"Exchange: %s \n" \
"Visit the website (www.randomstock.net) for more random stocks and funny quotes! \n" \
"%s" % (greetings, symbol, name, exchange, goodbye)


api.update_status(tweet)

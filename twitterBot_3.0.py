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

conn = sqlite3.connect('randomstock.db')
db = conn.cursor()




stock = random.randint(1, 25514)

# extract random stock from database for other markets

db.execute("SELECT exchange FROM securities WHERE id = ?", (stock,))
exchange = db.fetchone()
db.execute("SELECT symbol FROM securities WHERE id = ?", (stock,))
otherSymbol = db.fetchone()
db.execute("SELECT name FROM securities WHERE id = ?", (stock,))
otherStock = db.fetchone()
symbol = otherSymbol[0]
name = otherStock[0]
exchange = exchange[0]


# extract random stock from pennyStock database



tweet = "%s Todays Random Stock is: \n" \
"Symbol: %s \n" \
"Company: %s \n" \
"Exchange: %s \n" \
"%s" % (greetings, symbol, name, exchange, goodbye)


api.update_status(tweet)

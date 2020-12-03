import time
import tweepy as tp
import random


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
def sleeper():
    int = random.randint(240, 300)
    time.sleep(int)


while 1 == 1:

    superUsers = ["PeterLBrandt", "SJosephBurns", "SeekingAlpha", "business", "traderstewie", "elerianm", "NicTrades", "50Pips", "MrAaronKlein", "ritholtz", "Rayner_Teo", "Schuldensuehner", "jsblokland", "steve_hanke", "TheStalwart", "EddyElfenbein", "Ralph_Acampora", "MebFaber", "Trader_Dante", "sspencer_smb", "StockCats", "LiveSquawk", "jimcramer"]
    for user in superUsers:
        print(user)
        for follower in api.followers(user):
            print(follower.screen_name)

            try:
                user_ID = follower.id
                api.create_friendship(user_ID)
                sleeper()

            except tp.error.TweepError:
                print(tp.error.TweepError)
                pass

    time.sleep(604800)

    user = api.get_user("UnplannedI")
    followers = api.followers_ids("UnplannedI")
    following = api.friends_ids("UnplannedI")

    for person in following:

        if person not in followers:

            try:
                api.destroy_friendship(person)
                sleeper()
            except tp.error.TweepError:
                pass
        else:
            pass

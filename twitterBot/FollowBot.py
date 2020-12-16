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

user = api.get_user("business")
for follower in user.followers():

    if not follower.following:

        try:
            user_ID = follower.id
            api.create_friendship(user_ID)
            sleeper()
        except tp.error.TweepError:
            pass


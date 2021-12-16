import tweepy

# Authenticate to Twitter
auth = tweepy.OAuthHandler("WESM4XEo8vZYv5AARe4gdNWTA", 
    "VwxQHFdpFr5elAcEYVIiAF7daX6opH04HemyLSyeC2aUehlf92")
auth.set_access_token("1455271107897004037-trpcifKKBpUrlEbOvFPqt4sw2CSXq6", 
"kHYrzrpwtLso2cAqBuh9I1xiXhLQFz7oNAVARunnKNp8N")

api = tweepy.API(auth)

#Create API object
#api = tweepy.API(auth, wait_on_rate_limit=True,
  #  wait_on_rate_limit_notify=True)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")


for tweet in api.search_tweets(q="#amazon #climatechange", lang="en", rpp=10):
    print(f"{tweet.user.name}:{tweet.text}")


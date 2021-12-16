import tweepy
import threading

class Scraper(threading.Thread):

    def __init__(self, company_name):
        threading.Thread.__init__(self)
        self.search = company_name + " #climatechange"

        # Authenticate to Twitter
        auth = tweepy.OAuthHandler("WESM4XEo8vZYv5AARe4gdNWTA", 
            "VwxQHFdpFr5elAcEYVIiAF7daX6opH04HemyLSyeC2aUehlf92")
        auth.set_access_token("1455271107897004037-trpcifKKBpUrlEbOvFPqt4sw2CSXq6", 
        "kHYrzrpwtLso2cAqBuh9I1xiXhLQFz7oNAVARunnKNp8N")

        self.api = tweepy.API(auth)

        try:
            self.api.verify_credentials()
            print("Authentication OK")
        except:
            print("Error during authentication")

    def run(self):
        print("SEARCH TERM = " + self.search)
        for tweet in self.api.search_tweets(q=self.search, lang="en", count=10):
            print(f"{tweet.user.name}:{tweet.text}")


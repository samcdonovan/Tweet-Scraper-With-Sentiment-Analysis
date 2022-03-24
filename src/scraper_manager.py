from tweet_dao import TweetDAO
import tweepy
import os


class ScraperManager():

    def __init__(self, scraper_list, tweet_dao):
        self.scraper_list = scraper_list

        self.thread_complete_count = 0

        # Authenticate Twitter API with environment variables
        auth = tweepy.OAuthHandler(
            os.getenv('TWITTER_CONSUMER'), os.getenv('TWITTER_CONSUMER_SECRET'))

        auth.set_access_token(os.getenv('TWITTER_ACCESS'),
                              os.getenv('TWITTER_ACCESS_SECRET'))

        api = tweepy.API(auth)
       

        try:
            api.verify_credentials()
            print("Authentication OK")
        except Exception as ex:
            print("Error during authentication: " + ex)

        for scraper in self.scraper_list:

            scraper.setup(tweet_dao, api)

    def start_threads(self):

        for scraper in self.scraper_list:
            scraper.start()

        # self.finalise()

    def check_completed_threads(self):
        thread_complete_count = 0

        for scraper in self.scraper_list:
            if scraper.is_thread_complete():
                thread_complete_count += 1

        self.thread_complete_count = thread_complete_count

    def get_thread_complete_count(self):
        return self.thread_complete_count

    def start_single_thread(self, company_name):
        for scraper in self.scraper_list:
            if scraper.company_name == company_name:
                scraper.get_tweets()

    def finalise(self):
        for scraper in self.scraper_list:
            scraper.set_thread_complete(True)

        print("Finalising, please wait while threads finish current activity..." )
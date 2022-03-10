from concurrent.futures import thread
from tweet_dao import TweetDAO
import tweepy
import os
##from textblob import TextBlob, Word
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

class ScraperManager():

    def __init__(self, scraper_list, tweet_dao):
        self.scraper_list = scraper_list

        tweet_dao.init_db()
        # Authenticate Twitter API with environment variables
        auth = tweepy.OAuthHandler(os.getenv('TWITTER_CONSUMER'), os.getenv('TWITTER_CONSUMER_SECRET'))

        auth.set_access_token(os.getenv('TWITTER_ACCESS'), os.getenv('TWITTER_ACCESS_SECRET'))
       
        api = tweepy.API(auth)
        wnl = WordNetLemmatizer()
        wordnet.ensure_loaded()
        
        try:
            api.verify_credentials()
            print("Authentication OK")
        except Exception as ex:
            print("Error during authentication: " + ex)

        for scraper in self.scraper_list:
        
            scraper.setup(tweet_dao, api, wnl, wordnet, nltk)

    def start_threads(self):
       
        for scraper in self.scraper_list:
            scraper.start()
        
        #self.finalise()

    def finalise(self):
        thread_complete_count = 0
        while thread_complete_count < len(self.scraper_list):
            thread_complete_count = 0
            for scraper in self.scraper_list:
                if scraper.is_thread_complete():
                    thread_complete_count += 1    

        self.scraper_list[0].tweet_dao.close_connection()

    def start_single_thread(self, company_name):
        for scraper in self.scraper_list:
            if scraper.company_name == company_name:
                scraper.get_tweets()
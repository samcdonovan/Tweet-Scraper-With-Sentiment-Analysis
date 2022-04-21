from audioop import mul
import tweepy
import threading
import time
from threading import Thread
import datetime
import tweet


class Scraper():
    search_tweets = []

    def __init__(self, company_name):
        Thread.__init__(self)

        self.timeline = "new"
        self.count = 100

        self.company_name = company_name
        self.search_terms = [company_name + " Climate Change" + " -filter:retweets", "#" + company_name + " climate change -filter:retweets",
                             "#" + company_name + " #ClimateChange -filter:retweets", company_name + " #ClimateChange -filter:retweets"]
        self.thread_complete = False

    def setup(self, tweet_dao, api):
        self.tweet_dao = tweet_dao

        self.api = api

    def run(self):

        while len(self.search_terms) > 0 and not self.thread_complete:

            time.sleep(5)
            self.search = self.search_terms.pop()
            self.search_tweets = []
            self.get_tweets()

            tweet_number = 0
            while len(self.search_tweets) > 0 and not self.thread_complete:
                # for search_tweet in self.search_tweets:
                tweet_number += 1

                print("Tweet no.: " + str(tweet_number))
                self.clean_and_add_to_db(self.search_tweets.pop(0))

        self.thread_complete = True

    def is_thread_complete(self):
        return self.thread_complete

    def sum_up_to(self, number):
        return sum(range(1, number + 1))

    def set_thread_complete(self, thread_check):
        self.thread_complete = thread_check

    def get_tweets(self):
        today = datetime.datetime.now().replace(
            hour=23, minute=59, second=59, microsecond=999999)

        today += datetime.timedelta(1)
        newest_timestamp = self.tweet_dao.get_newest_tweet(self.company_name)[
            1]

        if newest_timestamp is None:
            number_of_days = 7
        else:
            number_of_days = (today - newest_timestamp).days
            if number_of_days > 7:
                number_of_days = 7
        #oldest_id = self.tweet_dao.get_tweet_id_with_date(
         #   "MIN", current_day_in_week, self.company_name)
        oldest_id = 0
        number_of_days = 7
        for day_index in range(number_of_days + 1, 0, -1):
           
            current_day_in_week = today - datetime.timedelta(day_index)
            
            try:
                tweets = self.api.search_tweets(
                    q=self.search, lang="en", count=self.count, tweet_mode="extended",
                    until=current_day_in_week.date(), since_id = oldest_id)
                    
                self.search_tweets.extend(tweets) # extend search_tweets by adding the retrieved Tweets
    
                oldest_id = self.search_tweets[-1].id
            except:
                continue

            if len(self.search_tweets) > 0:
                oldest_id = self.search_tweets[0].id

    def stop(self):
        self.thread.stop()

    def start(self):

        print(self.company_name + " thread started.")
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def clean_and_add_to_db(self, scraped_tweet):
        self.tweet_dao.add_to_database(tweet.Tweet(
            scraped_tweet.id, self.company_name, scraped_tweet.full_text, scraped_tweet.created_at))



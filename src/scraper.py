import tweepy  # Twitter API library
import threading
from threading import Thread
import time  # used for sleep functionality
import datetime  # used to manipulate the dates of the retrieved Tweets
import tweet  # local class


class Scraper():
    """Scraper class for retrieving Tweets from the Twitter API using Tweepy"""
    search_tweets = []

    def __init__(self, company_name):
        """
        Initialises the scraper object by setting class variables used for Twitter API search.

            Parameters:
                company_name (string): The name of the company that the current scraper is for.
        """
        Thread.__init__(self)

        self.count = 100  # max number of Tweets per query (capped at 100)

        self.company_name = company_name

        # set the different search terms for the API query. There are 4 different variations with or without hashtags.
        self.search_terms = [company_name + " Climate Change" + " -filter:retweets", "#" + company_name + " climate change -filter:retweets",
                             "#" + company_name + " #ClimateChange -filter:retweets", company_name + " #ClimateChange -filter:retweets"]

        self.thread_complete = False  # set thread complete flag to false

    def setup(self, dao, api):
        """
        Sets the data access object and Twitter API object.

            Parameters:
                dao (data_access_object): Data access object for connecting to and querying the local MySQL database. Implemented locally.
                api (Tweepy API object): Tweepy object used for connecting to the API and querying.
        """

        # set class variables
        self.dao = dao
        self.api = api

    def run(self):
        """
        Main function that runs the current scraper. This function is run using a Thread. 
        """

        # loop while there are still search terms left in the search terms list and
        # while the thread complete flag is still false
        while len(self.search_terms) > 0 and not self.thread_complete:

            time.sleep(5)  # sleep the Thread for 5 seconds for crawl delay
            self.search = self.search_terms.pop()  # pop the last search term from the list
            self.search_tweets = []  # empty the tweets list
            self.get_tweets()  # repopulate tweets list with new tweets

            tweet_number = 0  # for printing to console

            # loop while there are still tweets in self.search_tweets and while the thread complete flag is still false
            while len(self.search_tweets) > 0 and not self.thread_complete:

                tweet_number += 1

                print("Tweet no.: " + str(tweet_number))

                # pop the first Tweet from self.search_tweets and add it to the database
                self.add_to_db(self.search_tweets.pop(0))

        self.thread_complete = True

    def is_thread_complete(self):
        """
        Retrieves the thread complete flag.
            Returns:
                self.thread_complete (boolean): True or false depending on whether the scraper is complete.
        """
        return self.thread_complete

    def set_thread_complete(self, thread_check):
        """
        Sets the thread complete flag to true or false

            Parameters:
                thread_check (boolean): True or false depending on whether the scraper should be running or not.
        """
        self.thread_complete = thread_check

    def get_tweets(self):
        """
        Main function for retrieving Tweets from the Twitter API. Uses datetime to manipulate
        the maximise number of collected Tweets.
        """

        today = datetime.datetime.now().replace(
            hour=23, minute=59, second=59, microsecond=999999)  # get last minute of today's date

        today += datetime.timedelta(1)  # add 1 to account for indexing

        newest_timestamp = self.dao.get_newest_tweet(
            self.company_name)[1]  # get date of most recent Tweet in DB

        if newest_timestamp is None:
            number_of_days = 7
        else:

            # get the number of days from today that the most recent Tweet was collected
            number_of_days = (today - newest_timestamp).days

            if number_of_days < 7:
                number_of_days = 7

        # oldest_id = self.tweet_dao.get_tweet_id_with_date(
         #   "MIN", current_day_in_week, self.company_name)
        oldest_id = 0
        number_of_days = 7

        # loop through every day in the past week
        for day_index in range(number_of_days + 1, 0, -1):

            current_day_in_week = today - datetime.timedelta(day_index)

            try:

                # use the current search term to retrieve Tweets.
                # until retrieves Tweets from dates prior to the specified date
                # since_id retrieves Tweets after the given ID
                tweets = self.api.search_tweets(
                    q=self.search, lang="en", count=self.count, tweet_mode="extended",
                    until=current_day_in_week.date() + datetime.timedelta(1), since_id=oldest_id)

                # extend search_tweets by adding the retrieved Tweets
                self.search_tweets.extend(tweets)

            except Exception as ex:
                # if there is an exception, print it and continue
                print("Tweepy error: " + str(ex))
                continue

            if len(self.search_tweets) > 0:
                # get most recent ID from the pulled Tweets
                oldest_id = self.search_tweets[-1].id

    def start(self):
        """
        Starts the thread for this scraper.
        """
        print(self.company_name + " thread started.")  # prints the name of the thread
        self.thread = threading.Thread(
            target=self.run)  # thread target is run()
        self.thread.start()  # start the thread

    def stop(self):
        """
        Stops the thread for this scraper.
        """
        self.thread.stop()

    def add_to_db(self, scraped_tweet):
        '''
        Creates a new Tweet object and then adds that Tweet to the MySQL database.

            Parameters:
                scraped_tweet (Tweepy object): The current Tweet to add to the database
        '''

        # create a new Tweet object using the relevant information from the Tweet,
        # and call add_to_database from the data access object
        self.dao.add_to_database(tweet.Tweet(
            scraped_tweet.id, self.company_name, scraped_tweet.full_text, scraped_tweet.created_at))

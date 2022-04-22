import os  # retrieves local .env variables
import tweepy  # Twitter API library


class ScraperManager():
    """Manager class for the 5 scrapers. Handles control over the scrapers."""

    def __init__(self, scraper_list, data_access_object):
        """
        Scraper manager initialisation function. 

            Parameters:
                scraper_list (scraper[]): List containing the 5 scrapers, one for each company.
                data_access_object (data_access_object object): The object which allows the scrapers to use the MySQL DB.
        """

        self.scraper_list = scraper_list

        # initialise number of threads that have been completed to 0
        self.thread_complete_count = 0

        # authenticate Twitter API with local environment variables
        auth = tweepy.OAuthHandler(
            os.getenv('TWITTER_CONSUMER'), os.getenv('TWITTER_CONSUMER_SECRET'))

        auth.set_access_token(os.getenv('TWITTER_ACCESS'),
                              os.getenv('TWITTER_ACCESS_SECRET'))

        api = tweepy.API(auth)  # setup Tweepy with auth variables

        try:
            api.verify_credentials()  # varify credentials
            print("Twitter authentication OK")
        except Exception as ex:
            print("Error during Twitter authentication: " + ex)

        # loop through each scraper in the scraper list
        for scraper in self.scraper_list:

            # set each scraper's DAO and Tweepy API
            scraper.setup(data_access_object, api)

    def start_threads(self):
        """
        Starts each scraper thread in the scraper list.
        """
        for scraper in self.scraper_list:
            scraper.start()

    def check_completed_threads(self):
        """
        Counts the number of completed threads and updates the thread_complete_count class variables.
        """

        thread_complete_count = 0

        for scraper in self.scraper_list:

            # if thread is complete, increment complete count by 1
            if scraper.is_thread_complete():
                thread_complete_count += 1

        self.thread_complete_count = thread_complete_count

    def get_thread_complete_count(self):
        """
        Retrieves the number of Threads that have completed.
            Returns:
                self.thread_complete_count (integer): The number of Threads that are completed.
        """
        return self.thread_complete_count

    def finalise(self):
        """
        Finalises all currently running Threads.
        """

        for scraper in self.scraper_list:
            # loops through each scraper and sets thread complete flag to True
            scraper.set_thread_complete(True)

        print("Finalising, please wait while threads finish current activity...")

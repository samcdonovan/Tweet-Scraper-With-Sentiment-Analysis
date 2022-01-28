
class ScraperManager():

    def __init__(self, scraper_list, tweet_dao):
        self.scraper_list = scraper_list
        self.tweet_dao = tweet_dao

    def start_threads(self):
        print(self.scraper_list)
        for scraper in self.scraper_list:
            scraper.run()

    def finalise(self):
        self.tweet_dao.save_and_close_database()
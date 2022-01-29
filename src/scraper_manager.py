
class ScraperManager():

    def __init__(self, scraper_list, tweet_dao):
        self.scraper_list = scraper_list

        tweet_dao.init_db()

        for scraper in self.scraper_list:
            scraper.set_dao(tweet_dao)

    def start_threads(self):
        print(self.scraper_list)
        for scraper in self.scraper_list:
            scraper.run()

    def finalise(self):
        self.scraper_list[0].tweet_dao.close_connection()



class ScraperManager():

    def __init__(self, scraper_list):
        self.scraper_list = scraper_list

    def start_threads(self):
        print(self.scraper_list)
        for scraper in self.scraper_list:
            scraper.run()
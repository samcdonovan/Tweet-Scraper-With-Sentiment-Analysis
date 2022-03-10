
from tweet import Tweet
from tweet_dao import TweetDAO
import scraper
import scraper_manager

dao = TweetDAO()

scraper_amazon = scraper.Scraper("amazon")
scraper_facebook = scraper.Scraper("facebook")
scraper_netflix = scraper.Scraper("netflix")
scraper_google = scraper.Scraper("google")

scraper_list = [scraper_amazon, scraper_facebook,
                scraper_netflix, scraper_google]

manager = scraper_manager.ScraperManager(scraper_list, dao)

manager.start_threads()
try:
    while manager.get_thread_complete_count() < len(scraper_list):
        manager.check_completed_threads()
        
except KeyboardInterrupt:
     print("Aborting program...")


manager.finalise()

print("All threads stopped and database connections closed." )
#exit = 2

# if __name__ == '__main__':
# manager.start_threads()
# pool = Pool()                         # Create a multiprocessing Pool
#pool.map(process_image, data_inputs)

  # do stuff, e.g. getting other user input()

 


if not exit:
    print("true")

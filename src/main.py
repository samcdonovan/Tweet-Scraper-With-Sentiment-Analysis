import requests
from tweet import Tweet
from tweet_dao import TweetDAO
import scraper
import scraper_manager

#response = requests.get('https://httpbin.org/ip')

#print('Your IP is {0}'.format(response.json()['origin']))

dao = TweetDAO()
#dao.init_db()
#dao.add_to_database(Tweet("TEST", "TEST", "TEST", "TEST"))
#dao.close_connection()

scraper_amazon = scraper.Scraper("amazon")
scraper_facebook = scraper.Scraper("facebook")
scraper_netflix = scraper.Scraper("netflix")
scraper_google = scraper.Scraper("google")

#scraper_amazon.get_list_of_dates()

scraper_list = [scraper_amazon, scraper_facebook, scraper_netflix, scraper_google]
#scraper_list = [scraper_google]

manager = scraper_manager.ScraperManager(scraper_list, dao)

manager.start_threads()
#manager.start_single_thread("amazon")
#manager.finalise()

exit = 2

#if __name__ == '__main__':
 # manager.start_threads()
    #pool = Pool()                         # Create a multiprocessing Pool
    #pool.map(process_image, data_inputs)

if not exit:
  print("true")
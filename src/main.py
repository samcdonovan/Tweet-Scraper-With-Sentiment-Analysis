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
scraper_google = scraper.Scraper("google")

scraper_list = [scraper_amazon, scraper_facebook, scraper_google]
#scraper_list = [scraper_google]

manager = scraper_manager.ScraperManager(scraper_list, dao)

manager.start_threads()

manager.finalise()

exit = 2

if not exit:
  print("true")
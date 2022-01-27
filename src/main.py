import requests
import tweet_dao
import scraper
import scraper_manager

#response = requests.get('https://httpbin.org/ip')

#print('Your IP is {0}'.format(response.json()['origin']))

#scraper_amazon = scraper.Scraper("#amazon")
#scraper_facebook = scraper.Scraper("#facebook")
scraper_google = scraper.Scraper("#google")

#scraper_list = [scraper_amazon, scraper_facebook, scraper_google]
scraper_list = [scraper_google]
manager = scraper_manager.ScraperManager(scraper_list)

manager.start_threads()

dao = tweet_dao.TweetDAO()

dao.init_db()

exit = 2

if not exit:
  print("true")
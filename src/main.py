
from tweet import Tweet
from tweet_dao import TweetDAO
import scraper
import scraper_manager
import naive_bayes
dao = TweetDAO()

import utility

#utility.training_and_test_to_csv()
#utility.training_csv()
#naive_bayes.cross_valdation()
#naive_bayes.run_scikit()
#naive_bayes.get_frequencies()

"""
tweetdao = TweetDAO()
tweetdao.clean_tweets_in_db()
"""

#naive_bayes.run_naive_bayes()
utility.plot_word_clouds()
#utility.plot_pie_charts()
#utility.plot_stacked_area()
#utility.plot_line_chart()
#naive_bayes.run_scikit()
#utility.create_csv()
"""
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
    print("--------------------------")
    print("Aborting program...")

manager.finalise()

naive_bayes.run_naive_bayes()
"""
print("All threads stopped and database connections closed.")
print("--------------------------")

if not exit:
    print("true")


# local files
from tweet import Tweet
from data_access_object import DAO
import scraper
import scraper_manager
import naive_bayes
dao = DAO()

import utility

user_input = ''

# text-based user input menu for running the system
while user_input != '0':
    print()
    print("Menu:")
    print("-------------------------------------")
    print()
    print("1. Collect Tweets")
    print("2. Run Naive Bayes")
    print("3. Run cross-validation")
    print("4. Visualise data")
    print("5. Clean database Tweets")
    print("0. Exit")
    print()
    print("-------------------------------------")

    user_input = input("Choose one of the above options: ") 

    # collect Tweets using API
    if user_input == "1":
        scraper_amazon = scraper.Scraper("amazon")
        scraper_facebook = scraper.Scraper("facebook")
        scraper_netflix = scraper.Scraper("netflix")
        scraper_google = scraper.Scraper("google")


        scraper_apple = scraper.Scraper("apple")

        scraper_list = [scraper_apple]
        scraper_list = [scraper_amazon, scraper_facebook,
                        scraper_netflix, scraper_google, scraper_apple]


        manager = scraper_manager.ScraperManager(scraper_list, dao)

        manager.start_threads()
        try:
            while manager.get_thread_complete_count() < len(scraper_list):
                manager.check_completed_threads()

        except KeyboardInterrupt:
            print("--------------------------")
            print("Aborting program...")

        manager.finalise()

        print("All threads stopped and database connections closed.")
        print("--------------------------")
    elif user_input == "2":
        # run Naive Bayes algorithm on Tweets in MySQL database
        naive_bayes.run_naive_bayes()
    elif user_input == "3":
        utility.create_training_csv() # get training set
        naive_bayes.cross_valdation() # run cross validation on local implementation
        naive_bayes.run_scikit() # run scikit-learns Naive Bayes
    elif user_input == "4":

        # plot word clouds, pie charts and scatter charts
        utility.plot_word_clouds()
        utility.plot_pie_charts()
        utility.plot_line_chart()
    elif user_input == "5":
        dao.clean_tweets_in_db()
    elif user_input == "0":
        print()
        print("Closing program...")
    else:
        print("Not recognized, please try again.")


if not exit:
    print("true")


from re import S
from tabnanny import check
import time
from mysql.connector import errorcode
import datetime
import mysql.connector
import utility


class TweetDAO():

    def new_connection(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database='scraped_tweets'
            )

            return connection

        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Username or password does not match.")
            elif error.errno == errorcode.ER_BAD_DB_ERROR:
                print("Cannot locate database.")
            else:
                print("Database error: ")
                print(error)

            return None

    def set_cursor(self, cursor):
        self.cursor = cursor

    def get_tweet_id_with_date(self, min_or_max, current_date, company_name):
        previous_date = current_date - datetime.timedelta(1)
        query = "SELECT " + min_or_max + "(id) FROM tweets WHERE company='" + company_name + \
            "' AND timestamp BETWEEN '%s' and '%s'" % (
                previous_date, current_date)

        connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database='scraped_tweets'
        )
        #connection = self.new_connection()

        cursor = connection.cursor(buffered=True)
        cursor.execute(query)
        tweet_id = cursor.fetchone()
        if tweet_id[0] is None:
            query = "SELECT MAX(id) FROM tweets WHERE company='" + \
                company_name + "' AND timestamp <= '%s'" % (previous_date)
            cursor.execute(query)
            tweet_id = cursor.fetchone()

        cursor.close()
        connection.close()
        return tweet_id

    def get_newest_tweet(self, company_name):
        query = "SELECT MAX(id), MAX(timestamp) FROM tweets WHERE timestamp = (SELECT MAX(timestamp) FROM tweets WHERE company='" + company_name + "')"

        #connection = self.new_connection()
        connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database='scraped_tweets'
        )
        cursor = connection.cursor(buffered=True)

        try:

            time.sleep(2)

            cursor.execute(query)

            tweet = cursor.fetchone()

            cursor.close()
            connection.close()
            return tweet
        except mysql.connector.Error as error:
            print("SQL database error: " + str(error))
            cursor.close()
            connection.close()
            return None

    def get_tweet_id(self, min_or_max):
        query = "SELECT " + min_or_max + "(id) FROM tweets"
        self.cursor.execute(query)

        return self.cursor.fetchone()

    def add_to_database(self, tweet):
        #connection = self.new_connection()
        connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database='scraped_tweets'
        )

        cursor = connection.cursor(buffered=True)
        check_unique = "SELECT * FROM tweets WHERE id = " + \
            str(tweet.unique_id)
        cursor.execute(check_unique)

        check_result = cursor.fetchall()

        if len(check_result) > 0:
            print("Tweet with ID " + str(tweet.unique_id) +
                  " already exists in the database.")
            return None

        add_tweet = ("INSERT INTO tweets "
                     "(id, company, original_tweet, cleaned_tweet, timestamp)"
                     "VALUES (%s, %s, %s, %s, %s)")
        tweet_data = (tweet.unique_id, tweet.company,
                      tweet.original_tweet, tweet.cleaned_text, tweet.time)

        cursor.execute(add_tweet, tweet_data)

        connection.commit()
        cursor.close()
        connection.close()

    def close_connection(self):

        self.cursor.close()
        self.connection.close()
        print("Database connection closed.")

    def clean_tweets_in_db(self):
        query = "SELECT * FROM tweets"
        connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database='scraped_tweets'
        )

        cursor = connection.cursor(buffered=True)
       
        cursor.execute(query)

        check_result = cursor.fetchall()
     
        #for i in range(0, 5):
        for i in range(0,len(check_result)):
            #print(check_result[i])
            print(i)
            processed_text = ""
            processed_text = utility.clean_and_lemmatize(check_result[i][2])
            update_query = "UPDATE tweets SET cleaned_tweet = '%s' WHERE id = '%s'"% (processed_text,   check_result[i][0])
            cursor.execute(update_query)
            connection.commit()
            
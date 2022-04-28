
import time # for sleeping
from mysql.connector import errorcode
import mysql.connector # for DB connection
import utility # local file


class DAO():
    """
    Data Access Object class, for handling all MySQL DB queries and insertions.
    """

    def new_connection(self):
        """
        Creates and returns a new DB connection to the scraped_tweets DB.
            Returns:
                connection (MySQL connection): The newly created connection.
        """
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

    def get_newest_tweet(self, company_name):
        """
        Returns the newest Tweet in the DB for the specified company.
            Parameters:
                company_name (string): The name of the company.
            Returns:
                tweet (tweet object): The newest Tweet for that company.
        """

        # get Tweet with most recent timestamp for the company
        query = "SELECT MAX(id), MAX(timestamp) FROM tweets WHERE timestamp = (SELECT MAX(timestamp) FROM tweets WHERE company='" + company_name + "')"

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

    def add_to_database(self, tweet):
        """
        Inserts a Tweet into the scraped_tweets MySQL table.
            Parameters:
                tweet (tweet object): The Tweet to be inserted into the DB.
        """
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database='scraped_tweets'
        )

        cursor = connection.cursor(buffered=True)

        # query the DB for a Tweet with the ID of the specified Tweet
        check_unique = "SELECT * FROM tweets WHERE id = " + \
            str(tweet.unique_id)
        cursor.execute(check_unique)

        check_result = cursor.fetchall()

        # if the ID already exists in the table, break out of function
        if len(check_result) > 0:
            print("Tweet with ID " + str(tweet.unique_id) +
                  " already exists in the database.")
            return None

        # insert the new Tweet into the table
        add_tweet = ("INSERT INTO tweets "
                     "(id, company, original_tweet, cleaned_tweet, timestamp)"
                     "VALUES (%s, %s, %s, %s, %s)")
        tweet_data = (tweet.unique_id, tweet.company,
                      tweet.original_tweet, tweet.cleaned_text, tweet.time)

        cursor.execute(add_tweet, tweet_data)

        # close connection
        connection.commit()
        cursor.close()
        connection.close()

    def get_all_tweets(self):
        """
        Retrieves all of the Tweets from the database.
            Returns:
                tweets (list): List containing every row from scraped_tweets table.
        """

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database='scraped_tweets'
        )

        cursor = connection.cursor(buffered=True)

        # get every Tweet ordered by its timestamp
        query = "SELECT * FROM tweets ORDER BY timestamp ASC"

        cursor.execute(query)
        connection.commit()

        tweets = cursor.fetchall()
        cursor.close()
        connection.close()

        return tweets

    def add_sentiment_values(self, company_name, num_positive, num_negative, sentiment_values):
        """
        Uploads the sentiment values from sentiment analysis into the database.
            Parameters:
                company_name (string): The name of the company that these values belong to.
                num_positive (integer): The amount of positive Tweets about that company.
                num_negative (integer): The amount of negative Tweets about that company.
                sentiment_values (string): JSON string object containing individual date values.
        """
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database='scraped_tweets'
        )
        cursor = connection.cursor(buffered=True)

        # get all rows in sentiment_results table where the company is the specified company
        check_unique = "SELECT * FROM sentiment_results WHERE company = '" + company_name + "'"
        cursor.execute(check_unique)

        check_result = cursor.fetchall()

        if len(check_result) > 0:

            # if there already exists a row for the specified company, update it
            query = "UPDATE sentiment_results SET num_positive = '%s', num_negative = '%s', sentiment_values = '%s' WHERE company = '%s'" % (
                num_positive, num_negative, sentiment_values, company_name)

            cursor = connection.cursor(buffered=True)
            cursor.execute(query)

        else:
            # if a row does not yet exist for the specified company, insert it into the table.
            query = ("INSERT INTO sentiment_results "
                     "(num_positive, num_negative, company, sentiment_values)"
                     "VALUES (%s, %s, %s, %s)")

            cursor = connection.cursor(buffered=True)
            sentiment_data = (num_positive, num_negative,
                              company_name, sentiment_values)

            cursor.execute(query, sentiment_data)

        # close connection
        connection.commit()
        cursor.close()
        connection.close()

    def get_sentiment_values(self):
        """
        Retrieves the values obtained from sentiment analysis from the DB.
            Returns:
                sentiment_results (list): List containing all of the sentiment value rows in the DB.
        """
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database='scraped_tweets'
        )

        cursor = connection.cursor(buffered=True)

        query = "SELECT * FROM sentiment_results"  # get all rows

        cursor.execute(query)
        connection.commit()

        sentiment_results = cursor.fetchall()
        cursor.close()
        connection.close()

        return sentiment_results

    def clean_tweets_in_db(self):
        """
        Cleans and lemmatizes all of the Tweets currently stored in the DB.
        """
        query = "SELECT * FROM tweets"  # get every Tweet
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database='scraped_tweets'
        )

        # execute query through connection
        cursor = connection.cursor(buffered=True)
        cursor.execute(query)
        check_result = cursor.fetchall()

        # loop through each retrieved Tweet
        for pos in range(0, len(check_result)):

            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database='scraped_tweets'
            )
            cursor = connection.cursor(buffered=True)

            processed_text = ""
            processed_text = utility.clean_and_lemmatize(check_result[pos][2])

            # update current Tweet with newly cleaned and lemmatized text
            update_query = "UPDATE tweets SET cleaned_tweet = '%s' WHERE id = '%s'" % (
                processed_text, check_result[pos][0])

            try:
                cursor.execute(update_query)
            except Exception as ex:

                print("Query : " + update_query)
                print("Exception with " + str(pos) + " : " + str(ex))
                continue

            connection.commit()

    def close_connection(self):
        """
        Close the database connection
        """
        self.cursor.close()
        self.connection.close()
        print("Database connection closed.")

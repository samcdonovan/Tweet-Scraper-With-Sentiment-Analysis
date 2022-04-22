import utility

class Tweet:
    """Tweet class for storing Tweet data to be into the DB. Originally contained
    methods for cleaning the Tweet but these were moved to utility as they were useful
    outside of Tweet creation"""

    def __init__(self, unique_id, company, original_tweet, time):
        """
        Tweet initialisation method. Sets all relevant fields for DB insertion.
            Parameters:
                unique_id (integer): The unique ID of the Tweet, provided by Tweepy.
                company (string): The name of the company that the Tweet is about.
                original_tweet: The uncleaned text of the Tweet.
                time: The timestamp of the Tweet
        """

        self.unique_id = unique_id
        self.company = company
        self.original_tweet = original_tweet

        # clean and lemmatize the Tweet using the utility function
        self.cleaned_text = utility.clean_and_lemmatize(self.original_tweet)
        self.time = time

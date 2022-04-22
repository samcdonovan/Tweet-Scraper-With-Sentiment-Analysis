import unicodedata
import sys
import utility

class Tweet:

    def __init__(self, unique_id, company, original_tweet, time):
        self.unique_id = unique_id
        self.company = company
        self.original_tweet = original_tweet
        self.cleaned_text = utility.clean_and_lemmatize(self.original_tweet)
        self.tokenized = utility.tokenize(self.cleaned_text) 
        self.time = time


class Tweet:
    
    def __init__(self, unique_id, company, original_tweet, cleaned_text, time):
        self.unique_id = unique_id
        self.company = company
        self.original_tweet = original_tweet
        self.cleaned_text = cleaned_text
        self.time = time

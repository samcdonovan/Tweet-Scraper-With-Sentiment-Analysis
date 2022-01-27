
class Tweet:
    
    def __init__(self, id, company, original_tweet, cleaned_text, time):
        self.id = id
        self.company = company
        self.original_tweet = original_tweet
        self.cleaned_text = cleaned_text
        self.time = time

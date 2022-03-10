from audioop import mul
import tweepy
import threading
import time
from threading import Thread
import unicodedata
import sys
import datetime

import tweet


class Scraper():
    search_tweets = []

    def __init__(self, company_name):
        Thread.__init__(self)

        self.timeline = "new"
        self.count = 100

        self.company_name = company_name
        self.search_terms = [company_name + " Climate Change" + " -filter:retweets",
                             "#" + company_name + " #ClimateChange -filter:retweets", company_name + " #ClimateChange -filter:retweets"]
        self.thread_complete = False

    def setup(self, tweet_dao, api, wnl, wordnet, nltk):
        self.tweet_dao = tweet_dao
        self.tweet_dao.set_cursor(
            self.tweet_dao.connection.cursor(buffered=True))
        self.api = api
        self.wnl = wnl
        self.wordnet = wordnet
        self.nltk = nltk

    def run(self):
        
        for search in self.search_terms:

            time.sleep(5)
            self.search = search
            self.search_tweets = []
            self.get_tweets()

            tweet_number = 0

            for search_tweet in self.search_tweets:
                tweet_number += 1
                print("Tweet no.: " + str(tweet_number))
                self.get_tweet_obj(search_tweet)

    def is_thread_complete(self):
        return self.thread_complete

    def sum_up_to(self, number):
        return sum(range(1, number + 1))

    def get_tweets(self):
        today = datetime.datetime.now().replace(
            hour=23, minute=59, second=59, microsecond=999999)

        today += datetime.timedelta(1)
        newest_timestamp = self.tweet_dao.get_newest_tweet(self.company_name)[
            1]

        if newest_timestamp is None:
            number_of_days = 7
        else:
            number_of_days = (today - newest_timestamp).days
            if number_of_days > 7:
                number_of_days = 7

        oldest_id = self.tweet_dao.get_tweet_id_with_date(
            "MIN", today, self.company_name)

        for day_index in range(number_of_days, -1, -1):

            current_day_in_week = today - datetime.timedelta(day_index)

            tweets = self.api.search_tweets(
                q=self.search, lang="en", count=self.count, tweet_mode="extended", until=current_day_in_week.date(), since_id=oldest_id)
            self.search_tweets.extend(tweets)

            if len(self.search_tweets) > 0:
                oldest_id = self.search_tweets[0].id

    def stop(self):
        self.thread.stop()

    def start(self):

        print(self.company_name + " thread started.")
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def get_tweet_obj(self, search_tweet):

        converted_tweet = self.convert_to_list(search_tweet.full_text)

        tagged = self.nltk.pos_tag(converted_tweet)
        wordnet_tagged = list(
            map(lambda x: (x[0], self.pos_tagger(x[1])), tagged))

        lemmatized_sentence = []
        for word, tag in wordnet_tagged:
            if tag is None:
                # if there is no available tag, append the token as is
                lemmatized_sentence.append(word)
            else:
                # else use the tag to lemmatize the token
                lemmatized_sentence.append(self.wnl.lemmatize(word, tag))
        lemmatized_sentence = " ".join(lemmatized_sentence)

        self.tweet_dao.add_to_database(tweet.Tweet(
            search_tweet.id, self.company_name, search_tweet.full_text, lemmatized_sentence, search_tweet.created_at))

    def pos_tagger(self, nltk_tag):
        if nltk_tag.startswith('J'):
            return self.wordnet.ADJ
        elif nltk_tag.startswith('V'):
            return self.wordnet.VERB
        elif nltk_tag.startswith('N'):
            return self.wordnet.NOUN
        elif nltk_tag.startswith('R'):
            return self.wordnet.ADV
        else:
            return None

    def convert_to_list(self, sentence):
        converted_list = []
        stop_words = ["a", "about", "above", "after", "again", "against", "ain", "all", "am", "an", "and",
                      "any", "are", "aren", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between",
                      "both", "but", "by", "can", "couldn", "couldn't", "d", "did", "didn", "didn't", "do", "does", "doesn", "doesn't",
                      "doing", "don", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn", "hadn't",
                      "has", "hasn", "hasn't", "have", "haven", "haven't", "having", "he", "her", "here", "hers", "herself", "him",
                      "himself", "his", "how", "i", "if", "in", "into", "is", "isn", "isn't", "it", "it's", "its", "itself", "just",
                      "ll", "m", "ma", "me", "mightn", "mightn't", "more", "most", "mustn", "mustn't", "my", "myself", "needn", "needn't",
                      "no", "nor", "not", "now", "o", "of", "off", "on", "once", "only", "or", "other", "our", "ours", "ourselves", "out", "over",
                      "own", "re", "s", "same", "shan", "shan't", "she", "she's", "should", "should've", "shouldn", "shouldn't", "so", "some", "such",
                      "t", "than", "that", "that'll", "the", "their", "theirs", "them", "themselves", "then", "there", "these", "they", "this", "those", "through",
                      "to", "too", "under", "until", "up", "ve", "very", "was", "wasn", "wasn't", "we", "were", "weren", "weren't", "what", "when", "where", "which",
                      "while", "who", "whom", "why", "will", "with", "won", "won't", "wouldn", "wouldn't", "y", "you", "you'd", "you'll", "you're", "you've", "your",
                      "yours", "yourself", "yourselves", "could", "he'd", "he'll", "he's", "here's", "how's", "i'd", "i'll", "i'm", "i've", "let's", "ought", "she'd", "she'll",
                      "that's", "there's", "they'd", "they'll", "they're", "they've", "we'd", "we'll", "we're", "we've", "what's", "when's", "where's", "who's", "why's", "would",
                      "able", "abst", "accordance", "according", "accordingly", "across", "act", "actually", "added", "adj", "affected", "affecting", "affects", "afterwards", "ah",
                      "almost", "alone", "along", "already", "also", "although", "always", "among", "amongst", "announce", "another", "anybody", "anyhow", "anymore",
                      "anyone", "anything", "anyway", "anyways", "anywhere", "apparently", "approximately", "arent", "arise", "around", "aside", "ask",
                      "asking", "auth", "available", "away", "awfully", "b", "back", "became", "become", "becomes", "becoming", "beforehand", "begin",
                      "beginning", "beginnings", "begins", "behind", "believe", "beside", "besides", "beyond", "biol", "brief", "briefly", "c", "ca", "came",
                      "cannot", "can't", "cause", "causes", "certain", "certainly", "co", "com", "come", "comes", "contain", "containing", "contains",
                      "couldnt", "date", "different", "done", "downwards", "due", "e", "ed", "edu", "effect", "eg", "eight", "eighty", "either", "else",
                      "elsewhere", "end", "ending", "enough", "especially", "et", "etc", "even", "ever", "every", "everybody", "everyone", "everything",
                      "everywhere", "ex", "except", "f", "far", "ff", "fifth", "first", "five", "fix", "followed", "following", "follows", "former", "formerly",
                      "forth", "found", "four", "furthermore", "g", "gave", "get", "gets", "getting", "give", "given", "gives", "giving", "go", "goes", "gone",
                      "got", "gotten", "h", "happens", "hardly", "hed", "hence", "hereafter", "hereby", "herein", "heres", "hereupon", "hes", "hi", "hid", "hither",
                      "home", "howbeit", "however", "hundred", "id", "ie", "im", "immediate", "immediately", "importance", "important", "inc", "indeed", "index",
                      "information", "instead", "invention", "inward", "itd", "it'll", "j", "k", "keep", "keeps", "kept", "kg", "km", "know", "known", "knows", "l",
                      "largely", "last", "lately", "later", "latter", "latterly", "least", "less", "lest", "let", "lets", "like", "liked", "likely", "line", "little",
                      "'ll", "look", "looking", "looks", "ltd", "made", "mainly", "make", "makes", "many", "may", "maybe", "mean", "means", "meantime", "meanwhile", "merely",
                      "mg", "might", "million", "miss", "ml", "moreover", "mostly", "mr", "mrs", "much", "mug", "must", "n", "na", "name", "namely", "nay", "nd", "near",
                      "nearly", "necessarily", "necessary", "need", "needs", "neither", "never", "nevertheless", "new", "next", "nine", "ninety", "nobody", "non",
                      "none", "nonetheless", "noone", "normally", "nos", "noted", "nothing", "nowhere", "obtain", "obtained", "obviously", "often", "oh", "ok",
                      "okay", "old", "omitted", "one", "ones", "onto", "ord", "others", "otherwise", "outside", "overall", "owing", "p", "page", "pages", "part",
                      "particular", "particularly", "past", "per", "perhaps", "placed", "please", "plus", "poorly", "possible", "possibly", "potentially", "pp",
                      "predominantly", "present", "previously", "primarily", "probably", "promptly", "proud", "provides", "put", "q", "que", "quickly", "quite",
                      "qv", "r", "ran", "rather", "rd", "readily", "really", "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", "related",
                      "relatively", "research", "respectively", "resulted", "resulting", "results", "right", "run", "said", "saw", "say", "saying", "says", "sec",
                      "section", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sent", "seven", "several", "shall", "shed", "shes",
                      "show", "showed", "shown", "showns", "shows", "significant", "significantly", "similar", "similarly", "since", "six", "slightly", "somebody",
                      "somehow", "someone", "somethan", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specifically", "specified",
                      "specify", "specifying", "still", "stop", "strongly", "sub", "substantially", "successfully", "sufficiently", "suggest", "sup", "sure", "take",
                      "taken", "taking", "tell", "tends", "th", "thank", "thanks", "thanx", "thats", "that've", "thence", "thereafter", "thereby", "thered", "therefore",
                      "therein", "there'll", "thereof", "therere", "theres", "thereto", "thereupon", "there've", "theyd", "theyre", "think", "thou", "though", "thoughh",
                      "thousand", "throug", "throughout", "thru", "thus", "til", "tip", "together", "took", "toward", "towards", "tried", "tries", "truly", "try", "trying",
                      "ts", "twice", "two", "u", "un", "unfortunately", "unless", "unlike", "unlikely", "unto", "upon", "ups", "us", "use", "used", "useful", "usefully",
                      "usefulness", "uses", "using", "usually", "v", "value", "various", "'ve", "via", "viz", "vol", "vols", "vs", "w", "want", "wants", "wasnt", "way",
                      "wed", "welcome", "went", "werent", "whatever", "what'll", "whats", "whence", "whenever", "whereafter", "whereas", "whereby", "wherein", "wheres",
                      "whereupon", "wherever", "whether", "whim", "whither", "whod", "whoever", "whole", "who'll", "whomever", "whos", "whose", "widely", "willing",
                      "wish", "within", "without", "wont", "words", "world", "wouldnt", "www", "x", "yes", "yet", "youd", "youre", "z", "zero", "a's", "ain't", "allow",
                      "allows", "apart", "appear", "appreciate", "appropriate", "associated", "best", "better", "c'mon", "c's", "cant", "changes", "clearly",
                      "concerning", "consequently", "consider", "considering", "corresponding", "course", "currently", "definitely", "described", "despite",
                      "entirely", "exactly", "example", "going", "greetings", "hello", "help", "hopefully", "ignored", "inasmuch", "indicate", "indicated",
                      "indicates", "inner", "insofar", "it'd", "keep", "keeps", "novel", "presumably", "reasonably",
                      "second", "secondly", "sensible", "serious", "seriously", "sure", "t's", "third", "thorough", "thoroughly", "three", "well", "wonder"]

        for word in sentence.split():

            stop_check = bool(False)
            for stop_word in stop_words:
                if word.lower() in stop_word:
                    stop_check = bool(True)

            if not stop_check and "http" not in word:
                word = word.translate(dict.fromkeys(i for i in range(sys.maxunicode)
                                                    if unicodedata.category(chr(i)).startswith('P')))
               ## print("word: " +word + " --> " + wnl.lemmatize(word))
                converted_list.append(word)

        return converted_list

    # def get_tweets_old(self):
     #   if self.timeline == "new":

      #      self.search_tweets = self.api.search_tweets(
       #         q=self.search, lang="en", count=self.count, tweet_mode="extended")
        # elif self.timeline == "old":
        #   newest_id = self.tweet_dao.get_tweet_id("MAX")
        #  print("Oldest: " + str(newest_id))
        # self.search_tweets = self.api.search_tweets(
        #    q=self.search, lang="en", count=self.count, tweet_mode="extended", since_id=newest_id[0])

   # def scrape(self):
       # wnl = WordNetLemmatizer()

       # for search_tweet in self.api.search_tweets(q=self.search + " -filter:retweets", lang="en", count=10):

        #   converted_tweet = self.convert_to_list(search_tweet.text)

        #    tagged = nltk.pos_tag(converted_tweet)
        #    wordnet_tagged = list(
        #       map(lambda x: (x[0], self.pos_tagger(x[1])), tagged))

        #   lemmatized_sentence = []
        #  for word, tag in wordnet_tagged:
        #       if tag is None:
        # if there is no available tag, append the token as is
        #          lemmatized_sentence.append(word)
        #      else:
        # else use the tag to lemmatize the token
        #         lemmatized_sentence.append(wnl.lemmatize(word, tag))
        # lemmatized_sentence = " ".join(lemmatized_sentence)

        # print(self.company_name)
        # print(self.search)
        # self.tweet_dao.add_to_database(tweet.Tweet(
        #    search_tweet.id, self.company_name, search_tweet.text, lemmatized_sentence, search_tweet.created_at))
       # num_list = [1, 2, 3, 4]
        #self.process = multiprocessing.Process(target=heello(range(11)))
        # self.process.start()
       # self.pool = multiprocessing.Pool(50)
        #self.pool.apply_async(heello, range(11))
        #self.pool.map_async(heello, range(11))
        # results = [self.pool.apply_async(heello, (num))
        #          for num in num_list]
       # roots = [r.get() for r in results]
        # self.pool.close()
        # self.pool.terminate()
        # self.pool.join()

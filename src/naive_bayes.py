from distutils.command.build import build
import math
from operator import pos
import utility


def build_dictionary(dataset):
    dict = {}

    for tweet in dataset:
        for word in tweet.split(" "):
            if word in dict:
                dict[word] = dict[word] + 1
            else:
                dict[word] = 2


    return dict

def get_frequencies():
    positive_tweets = {"very good", "very amazing", "love"}
    negative_tweets = {"very bad", "very awful", "very hate"}
    positive_dict = build_dictionary(positive_tweets)   
    negative_dict = build_dictionary(negative_tweets)   

    for key in negative_dict.keys():
        if key not in positive_dict:
            positive_dict[key] = 1

    for key in positive_dict.keys():
        if key not in negative_dict:
            negative_dict[key] = 1

    positive_amount = 0

    for value in positive_dict.values():
        positive_amount += value

    negative_amount = 0

    for value in negative_dict.values():
        negative_amount += value

    print(positive_amount)    
    print(negative_amount) 
    print(positive_dict)
    print(negative_dict)

    pos_probs = {}
    #for value in positive_dict.values():
    for key in positive_dict:        
        pos_probs[key] = positive_dict[key] / positive_amount
        
    print(pos_probs)

    negative_probs = {}
    #for value in positive_dict.values():
    for key in negative_dict:        
        negative_probs[key] = negative_dict[key] / negative_amount
        
    print(negative_probs)
def get_counts(tokenized_text):
    counts = []

    #for i in range(len(tokenized_text)):


def calculate_probability(tokenized_text):
    counts = get_counts(tokenized_text)
    return math.log(counts / sum(counts))


def calculate_probability_other(tokenized_text):
    counts = get_counts(tokenized_text)
    return math.log(1/sum(counts))

"""
def sentiment(text):

calc_Sentiment < - function(review) {
    test < - tokenize(review)
  pos_pred < - sum( is .na(pos_probs[test])) * pos_probs_rare + sum(pos_probs[test], na.rm = TRUE)
  neg_pred < - sum( is .na(neg_probs[test])) * neg_probs_rare + sum(neg_probs[test], na.rm = TRUE)
    ifelse(pos_pred > neg_pred, "positive", "negative")
}
"""
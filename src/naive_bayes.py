
import math

import utility

    
def build_dictionary(dataset):
    dict = {}

    #for tweet in dataset:
    for index, row in dataset.iterrows():
      
        if not isinstance(row['text'], str):
            continue

        for word in row['text'].split(" "):
            if word in dict:
                dict[word] = dict[word] + 1
            else:
                dict[word] = 2

    return dict

def prior_probabilities(positive_tweets, negative_tweets):

    total = len(positive_tweets) + len(negative_tweets)

    positive = len(positive_tweets) / total
    negative = len(negative_tweets) / total

    dict = {"pos": positive , "neg": negative}
    return dict


def get_frequencies():
    #positive_tweets = {"very good", "very amazing", "love"}
    # negative_tweets = {"very bad", "very awful", "very hate"}
    train_tweets = utility.get_train()

    positive_tweets = train_tweets[train_tweets['target'] == 2]
    negative_tweets = train_tweets[train_tweets['target'] == -2]
   
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


    pos_probs = {}
    #for value in positive_dict.values():
    for key in positive_dict:        
        pos_probs[key] = positive_dict[key] / positive_amount
        

    negative_probs = {}
    #for value in positive_dict.values():
    for key in negative_dict:        
        negative_probs[key] = negative_dict[key] / negative_amount
        
    priors = prior_probabilities(positive_tweets, negative_tweets)

    #test_tweets = {"good good", "bad bad", "very bad", "love awful bad", "horrible good"}
    test_tweets = utility.get_test()
    
    #for tweet in test_tweets:
    correct_sum = 0
    missing = 0
    for index, row in test_tweets.iterrows():
        current_pos = priors["pos"]
        current_neg = priors["neg"]
        
        if not isinstance(row['text'], str):
            missing += 1
            continue

        for word in row['text'].split(" "):

            if word not in positive_dict.keys():
                positive_dict[word] = 1                
                pos_probs[word] = 1 / positive_amount
            if word not in negative_dict.keys():
                negative_dict[word] = 1                
                negative_probs[word] = 1 / negative_amount

            current_pos *= pos_probs[word]
            current_neg *= negative_probs[word]

        if current_pos > current_neg:
            sentiment = 2
        else:
            sentiment = -2
        
        if sentiment == row['target']:
            correct_sum += 1
        
        #print(row['text'] + ", target =  " + row['target'] + ", predicted = " + sentiment )

    print(str(correct_sum) + "/" + str(len(test_tweets) - missing) + " = " + str((correct_sum/(len(test_tweets) - missing))))



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
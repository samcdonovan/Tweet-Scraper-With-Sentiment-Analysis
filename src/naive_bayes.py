import math
import utility

positive_dict = {}
negative_dict = {}
prior_probs = {}
positive_probs = {}
negative_probs = {}
positive_amount = 0
negative_amount = 0

def build_table(dataset):
    table = {}
 
    for index, row in dataset.iterrows():
      
        if not isinstance(row['text'], str):
            continue

        for word in row['text'].split(" "):
            if word in table:
                table[word] = table[word] + 1
            else:
                table[word] = 2

    return table

def get_prior_probabilities(positive_tweets, negative_tweets):

    total = len(positive_tweets) + len(negative_tweets)

    positive = len(positive_tweets) / total
    negative = len(negative_tweets) / total

    global prior_probs
    prior_probs = {"pos": positive , "neg": negative}

def train():
    train_tweets = utility.get_train()

    positive_tweets = train_tweets[train_tweets['target'] == 2]
    negative_tweets = train_tweets[train_tweets['target'] == -2]
   
    global positive_dict
    global negative_dict

    positive_dict = build_table(positive_tweets)   
    negative_dict = build_table(negative_tweets)   

    for key in negative_dict.keys():
        if key not in positive_dict:
            positive_dict[key] = 1

    for key in positive_dict.keys():
        if key not in negative_dict:
            negative_dict[key] = 1
      
    get_prior_probabilities(positive_tweets, negative_tweets)

def get_conditional_probabilities():
    
    global positive_amount

    for value in positive_dict.values():
        positive_amount += value

    global negative_amount

    for value in negative_dict.values():
        negative_amount += value

    global positive_probs
    for key in positive_dict:        
        positive_probs[key] = positive_dict[key] / positive_amount
        
    global negative_probs
    for key in negative_dict:        
        negative_probs[key] = negative_dict[key] / negative_amount

def get_frequencies():

    train()

    get_conditional_probabilities()

    test_tweets = utility.get_test()
    
    num_correct = 0
    missing = 0
    for index, row in test_tweets.iterrows():
        current_positive = prior_probs["pos"]
        current_negative = prior_probs["neg"]
        
        if not isinstance(row['text'], str):
            missing += 1
            continue

        for word in row['text'].split(" "):

            if word not in positive_dict.keys():
                positive_dict[word] = 1                
                positive_probs[word] = 1 / positive_amount

            if word not in negative_dict.keys():
                negative_dict[word] = 1                
                negative_probs[word] = 1 / negative_amount

            current_positive *= positive_probs[word]
            current_negative *= negative_probs[word]

        if current_positive > current_negative:
            sentiment = 2
        else:
            sentiment = -2
        
        if sentiment == row['target']:
            num_correct += 1
        
    print(str(num_correct) + "/" + str(len(test_tweets) - missing) + " = " + str((num_correct/(len(test_tweets) - missing))))

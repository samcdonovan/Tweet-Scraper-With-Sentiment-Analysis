from tweet_dao import TweetDAO
import utility

"""
Global variables. This could have been made into a class, but this seemed more efficient.
"""
positive_dict = {}
negative_dict = {}
prior_probs = {}
positive_probs = {}
negative_probs = {}
positive_amount = 0
negative_amount = 0


def build_table(dataset):
    '''
    Returns a table containing the occurences for each word in the given dataset.

        Paramters:
            dataset (dataframe): The dataset to create a table for.

        Returns:    
            table (dictionary): Table containing the number of occurences for each word. 
    '''
    table = {}

    # iterate through each row in the dataset
    for index, row in dataset.iterrows():

        # the data cleaning can sometimes cause a row to have no text (very rarely),
        # so we coninue past rows that are empty
        if not isinstance(row['text'], str):
            continue

        # iterate through each word in the text of the current row
        for word in row['text'].split(" "):

            # increment by 1 if it already exists in the table
            if word in table:
                table[word] = table[word] + 1
            # otherwise set it to 2, this is to account for laplace smoothing
            else:
                table[word] = 2

    return table


def get_prior_probabilities(positive_tweets, negative_tweets):
    '''
    Gets the prior probabilities for the positive and negative classes. Does not return anything
    but does change the global variable, prior_probs

        Paramters:
            positive_tweets (dataframe): A dataframe containing positive Tweets from the training set.
            negative_tweets (dataframe): A dataframe containing negative Tweets from the training set. 
    '''

    # total number of Tweets in training set
    total = len(positive_tweets) + len(negative_tweets)

    # probability that any given Tweet in the dataset is positive or negative respectively
    positive = len(positive_tweets) / total
    negative = len(negative_tweets) / total

    global prior_probs # change prior_probs global variable
    prior_probs = {"pos": positive, "neg": negative}


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
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0

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

            if sentiment == 2:
                true_positive += 1
            elif sentiment == -2:
                true_negative += 1

            num_correct += 1
        
        else:
            if sentiment == 2:
                false_positive += 1
            elif sentiment == -2:
                false_negative += 1


    print(str(true_positive) + " | " + str(false_positive))
    print(str(false_negative) + " | " + str(true_negative))
    print(str(num_correct) + "/" + str(len(test_tweets) - missing) +
          " = " + str((num_correct/(len(test_tweets) - missing))))

def run_naive_bayes():
    dao = TweetDAO()
    train()

    get_conditional_probabilities()

    db_tweets = dao.get_all_tweets()

    missing = 0
    company_names = ['amazon', 'facebook', 'netflix', 'google']
    positive_predictions = {}
    negative_predictions = {}

    for company in company_names:
        positive_predictions[company] = 0
        negative_predictions[company] = 0

    for row in db_tweets:
        current_positive = prior_probs["pos"]
        current_negative = prior_probs["neg"]

        if not isinstance(row[3], str):
            missing += 1
            continue

        for word in row[3].split(" "):

            if word not in positive_dict.keys():
                positive_dict[word] = 1
                positive_probs[word] = 1 / positive_amount

            if word not in negative_dict.keys():
                negative_dict[word] = 1
                negative_probs[word] = 1 / negative_amount

            current_positive *= positive_probs[word]
            current_negative *= negative_probs[word]

        if current_positive > current_negative:
            positive_predictions[row[1]] += 1
        else:
            negative_predictions[row[1]] += 1
    
    
    for company in company_names:
        dao.add_sentiment_values(company, positive_predictions[company], negative_predictions[company])



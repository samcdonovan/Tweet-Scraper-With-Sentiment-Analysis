from data_access_object import DAO # local DB code
import utility # local utility code
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics
import json
import datetime

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

        Parameters:
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

        Parameters:
            positive_tweets (dataframe): A dataframe containing positive Tweets from the training set.
            negative_tweets (dataframe): A dataframe containing negative Tweets from the training set. 
    '''

    # total number of Tweets in training set
    total = len(positive_tweets) + len(negative_tweets)

    # probability that any given Tweet in the dataset is positive or negative respectively
    positive = len(positive_tweets) / total
    negative = len(negative_tweets) / total

    global prior_probs  # change prior_probs global variable
    prior_probs = {"pos": positive, "neg": negative}


def train(train_tweets):
    # train_tweets =

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


def cross_valdation():
    folds = utility.get_folds()
    average_confusion = {"true_positive": 0, "false_positive": 0,
                         "false_negative": 0, "true_negative": 0}
    average_accuracy = 0
    for key, value in folds.items():

        train(value["training"])
        get_conditional_probabilities()
        test_results = test(value['test'])
        print(key + ":")
        print(test_results["confusion"])
        print(str(test_results["accuracy"] * 100) + "%")

        average_confusion["true_positive"] += test_results["confusion"]["true_positive"] / \
            len(folds)
        average_confusion["false_positive"] += test_results["confusion"]["false_positive"] / \
            len(folds)
        average_confusion["true_negative"] += test_results["confusion"]["true_negative"] / \
            len(folds)
        average_confusion["false_negative"] += test_results["confusion"]["false_negative"] / \
            len(folds)

        average_accuracy += test_results["accuracy"]

    average_accuracy = average_accuracy / len(folds)

    print()
    print("Averages after " + str(len(folds)) + " folds: ")
    print(average_confusion)
    print(str(average_accuracy * 100) + "%")
    print()


def get_conditional_probabilities():

    global positive_amount
    positive_amount = 0
    for value in positive_dict.values():
        positive_amount += value

    global negative_amount
    negative_amount = 0
    for value in negative_dict.values():
        negative_amount += value

    global positive_probs
    positive_probs = {}
    for key in positive_dict:
        positive_probs[key] = positive_dict[key] / positive_amount

    global negative_probs
    negative_probs = {}
    for key in negative_dict:
        negative_probs[key] = negative_dict[key] / negative_amount


def test(test_tweets):
    num_correct = 0
    missing = 0

    confusion_matrix = {"true_positive": 0, "false_positive": 0,
                        "false_negative": 0, "true_negative": 0}

    for index, row in test_tweets.iterrows():
        current_positive = prior_probs["pos"]
        current_negative = prior_probs["neg"]

        if not isinstance(row['text'], str):
            missing += 1
            continue

        for word in row['text'].split(" "):
            laplace_smoothing(word)
            """
            if word not in positive_dict.keys():
                positive_dict[word] = 1
                positive_probs[word] = 1 / positive_amount

            if word not in negative_dict.keys():
                negative_dict[word] = 1
                negative_probs[word] = 1 / negative_amount
            """
            current_positive *= positive_probs[word]
            current_negative *= negative_probs[word]

        if current_positive > current_negative:
            sentiment = 2
        else:
            sentiment = -2

        if sentiment == row['target']:

            if sentiment == 2:
                #true_positive += 1
                confusion_matrix["true_positive"] += 1
            elif sentiment == -2:
                #true_negative += 1
                confusion_matrix["true_negative"] += 1

            num_correct += 1

        else:
            if sentiment == 2:
                confusion_matrix["false_positive"] += 1
                #false_positive += 1
            elif sentiment == -2:
                #false_negative += 1
                confusion_matrix["false_negative"] += 1

    accuracy = num_correct / (len(test_tweets) - missing)
    return {"confusion": confusion_matrix, "accuracy": accuracy}


def get_frequencies():

    train(utility.get_train())

    get_conditional_probabilities()

    test_tweets = utility.get_test()

    num_correct = 0
    missing = 0

    confusion_matrix = {"true_positive": 0, "false_positive": 0,
                        "false_negative": 0, "true_negative": 0}

    for index, row in test_tweets.iterrows():
        current_positive = prior_probs["pos"]
        current_negative = prior_probs["neg"]

        if not isinstance(row['text'], str):
            missing += 1
            continue

        for word in row['text'].split(" "):
            laplace_smoothing(word)
            """
            if word not in positive_dict.keys():
                positive_dict[word] = 1
                positive_probs[word] = 1 / positive_amount

            if word not in negative_dict.keys():
                negative_dict[word] = 1
                negative_probs[word] = 1 / negative_amount
            """
            current_positive *= positive_probs[word]
            current_negative *= negative_probs[word]

        if current_positive > current_negative:
            sentiment = 2
        else:
            sentiment = -2

        if sentiment == row['target']:

            if sentiment == 2:
                #true_positive += 1
                confusion_matrix["true_positive"] += 1
            elif sentiment == -2:
                #true_negative += 1
                confusion_matrix["true_negative"] += 1

            num_correct += 1

        else:
            if sentiment == 2:
                confusion_matrix["false_positive"] += 1
                #false_positive += 1
            elif sentiment == -2:
                #false_negative += 1
                confusion_matrix["false_negative"] += 1

    print(confusion_matrix)

    print(str(num_correct) + "/" + str(len(test_tweets) - missing) +
          " = " + str((num_correct/(len(test_tweets) - missing))))


def laplace_smoothing(word):
    global positive_dict
    global positive_probs
    global negative_dict
    global negative_probs

    if word not in positive_dict.keys():
        positive_dict[word] = 1
        positive_probs[word] = 1 / positive_amount

    if word not in negative_dict.keys():
        negative_dict[word] = 1
        negative_probs[word] = 1 / negative_amount


def run_naive_bayes():
    dao = DAO()
    train(utility.get_train())

    get_conditional_probabilities()

    db_tweets = dao.get_all_tweets()

    missing = 0
    company_names = ['amazon', 'facebook', 'netflix', 'google', 'apple']
    positive_predictions = {}
    negative_predictions = {}
    sentiment_values = {}

    for company in company_names:
        positive_predictions[company] = 0
        negative_predictions[company] = 0
        sentiment_values[company] = {}
        #sentiment_values[company]["positive"] = {}
        #sentiment_values[company]["negative"] = {}

    index = 0

    for row in db_tweets:
        current_positive = prior_probs["pos"]
        current_negative = prior_probs["neg"]

        if not isinstance(row[3], str):
            missing += 1
            continue

        for word in row[3].split(" "):
            laplace_smoothing(word)

            current_positive *= positive_probs[word]
            current_negative *= negative_probs[word]

        date = datetime.datetime.date(row[4])

        if str(date) not in sentiment_values[row[1]].keys():
            sentiment_values[row[1]][str(date)] = {"positive": 0, "negative": 0}
        if current_positive > current_negative:
            positive_predictions[row[1]] += 1
            sentiment_values[row[1]][str(date)]["positive"] += 1 
        else:
            negative_predictions[row[1]] += 1
            sentiment_values[row[1]][str(date)]["negative"] += 1
        
        #sentiment_values[row[1]][str(row[4])] = {}
        #sentiment_values[row[1]][index] = {}

        sentiment_json = {'positive':  (current_positive / (current_positive + current_negative)), 'negative': + (current_negative / (current_positive + current_negative))}
        #sentiment_json = {'positive': current_positive, 'negative': current_negative}




       # sentiment_values[row[1]][index] = sentiment_json
     
        index += 1

    for company in company_names:
        dao.add_sentiment_values(
            company, positive_predictions[company], negative_predictions[company], json.dumps(sentiment_values[company]))
    
def get_word_clouds():
    dao = DAO()

    train(utility.get_train())

    get_conditional_probabilities()

    db_tweets = dao.get_all_tweets()

    missing = 0
    company_names = ['amazon', 'facebook', 'netflix', 'google', 'apple']
    positive_predictions = {}
    negative_predictions = {}
    sentiment_values = {}

    for company in company_names:
        positive_predictions[company] = 0
        negative_predictions[company] = 0
        sentiment_values[company] = {}

    bag_of_words = {"positive_train":{}, "negative_train": {}, "positive_unseen": {}, "negative_unseen": {}}

    for row in db_tweets:
        current_positive = prior_probs["pos"]
        current_negative = prior_probs["neg"]

        if not isinstance(row[3], str):
            missing += 1
            continue

        for word in row[3].split(" "):
            laplace_smoothing(word)

            current_positive *= positive_probs[word]
            current_negative *= negative_probs[word]

        if current_positive > current_negative:
            positive_predictions[row[1]] += 1
            for word in row[3].split(" "):
                if word =="climate" or word=="change" or word=="global":
                    continue

                if word not in bag_of_words["positive_unseen"].keys():
                    bag_of_words["positive_unseen"][word] = 0
                    
                bag_of_words["positive_unseen"][word] += 1
            
        else:
            negative_predictions[row[1]] += 1
            for word in row[3].split(" "):
                if word =="climate" or word=="change" or word=="global":
                    continue

                if word not in bag_of_words["negative_unseen"].keys():
                    bag_of_words["negative_unseen"][word] = 0

                bag_of_words["negative_unseen"][word] += 1

    for word in sorted(positive_dict, key=positive_dict.get, reverse=True):
        if word == "climate" or word == "change" or word == "global":
            continue
        bag_of_words["positive_train"][word] = positive_dict[word]

    for word in sorted(negative_dict, key=negative_dict.get, reverse=True):
        if word =="climate" or word=="change" or word=="global":
            continue
        bag_of_words["negative_train"][word] = negative_dict[word]

    return bag_of_words

def run_scikit():
    #train_tweets = utility.get_train()
    vectorizer = CountVectorizer()
    folds = utility.get_folds()
    average_accuracy = 0
    for key, value in folds.items():
        train_tweets = value["training"]
        # train(value["training"])
        # get_conditional_probabilities()
        print(key + ":")

        # test(value['test'])
        nb = MultinomialNB(alpha=1.0, fit_prior=True)

        vectorizer.fit(train_tweets.text.astype('U'))

        train_array = vectorizer.transform(train_tweets.text.astype('U'))

        nb.fit(train_array, train_tweets.target)

        #test_tweets = utility.get_test()
        test_tweets = value["test"]
        test_vector = vectorizer.transform(test_tweets.text.astype('U'))
        test_predicted = nb.predict(test_vector)
        current_accuracy = metrics.accuracy_score(
            test_tweets.target, test_predicted)
        average_accuracy += current_accuracy

        print("Scikit-learn: " + str(current_accuracy * 100) + "%")

    print()
    print("Scikit avg. : " + str((average_accuracy / len(folds)) * 100) + "%")

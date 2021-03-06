from data_access_object import DAO  # local DB code
import utility  # local utility code

# Scikit-learn is used for accuracy comparison
from sklearn.naive_bayes import MultinomialNB 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics
import json
import datetime

"""
Global variables. This could have been made into a class, but globals seemed more efficient.
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


def calc_prior_probabilities(positive_tweets, negative_tweets):
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


def calc_conditional_probabilities():
    """
    Calculates conditional probabilities for each word in the positive and negative bag of words
    """

    # retrieve globals
    global positive_amount
    global negative_amount
    global positive_probs
    global negative_probs

    # sum the total number of positive words using term frequencies
    positive_amount = 0
    for value in positive_dict.values():
        positive_amount += value

    # sum the total number of negative words using term frequencies
    negative_amount = 0
    for value in negative_dict.values():
        negative_amount += value

    # calculate conitional probability for each word in the positive dictionary
    positive_probs = {}
    for key in positive_dict:
        positive_probs[key] = positive_dict[key] / positive_amount

    # calculate conitional probability for each word in the negative dictionary
    negative_probs = {}
    for key in negative_dict:
        negative_probs[key] = negative_dict[key] / negative_amount


def laplace_smoothing(word):
    """
    Performs Laplace smoothing on the specified word.
        Parameters:
            word (string): The word to perform Laplace smoothing for.
    """

    # retrieve global variables
    global positive_dict
    global positive_probs
    global negative_dict
    global negative_probs

    # if the word is not in the keys for the positive dictionary,
    # set its term frequency to 1 and caclulate its probability
    if word not in positive_dict.keys():
        positive_dict[word] = 1
        positive_probs[word] = 1 / positive_amount

    # if the word is not in the keys for the negative dictionary,
    # set its term frequency to 1 and caclulate its probability
    if word not in negative_dict.keys():
        negative_dict[word] = 1
        negative_probs[word] = 1 / negative_amount


def train(train_tweets):
    """
    Main function for training the term frequencies for the NB classifier.

        Parameters:
            train_tweets (dataframe): The Tweets to train the classifier on.
    """

    # seperate the positive and negative Tweets
    positive_tweets = train_tweets[train_tweets['target'] == 2]
    negative_tweets = train_tweets[train_tweets['target'] == -2]

    # retrieve global variables
    global positive_dict
    global negative_dict

    # train term frequencies for positive and negative words
    positive_dict = build_table(positive_tweets)
    negative_dict = build_table(negative_tweets)

    for key in negative_dict.keys():
        if key not in positive_dict:
            positive_dict[key] = 1

    for key in positive_dict.keys():
        if key not in negative_dict:
            negative_dict[key] = 1

    # set prior probabilities for positive and negative classes
    calc_prior_probabilities(positive_tweets, negative_tweets)


def run_naive_bayes():
    """
    Main function for running Naive Bayes on collected Tweets. After running it,
    the results are inserted into local MySQL database.
    """
    dao = DAO()  # get a DAO object to insert into DB
    train(utility.get_train())  # train the classifier

    calc_conditional_probabilities()  # calculate the conditional probabilities

    db_tweets = dao.get_all_tweets()  # get collected teets

    missing = 0
    company_names = ['amazon', 'facebook', 'netflix', 'google', 'apple']
    positive_predictions = {}
    negative_predictions = {}
    sentiment_values = {}

    # initiate predictions for all companies
    for company in company_names:
        positive_predictions[company] = 0
        negative_predictions[company] = 0
        sentiment_values[company] = {}

    # loop through every row in the DB
    for row in db_tweets:

        # set current positive and negative to their prior probabilities
        current_positive = prior_probs["pos"]
        current_negative = prior_probs["neg"]

        # if the current row is empty, skip this iteration
        if not isinstance(row[3], str):
            missing += 1
            continue

        # loop through each word in the current tweet
        for word in row[3].split(" "):
            laplace_smoothing(word)  # call Laplace smoothing on the word

            # multiplty the current probabilities by the conditional probabilities of the word
            current_positive *= positive_probs[word]
            current_negative *= negative_probs[word]

        # get date object for current row
        date = datetime.datetime.date(row[4])

        if str(date) not in sentiment_values[row[1]].keys():
            sentiment_values[row[1]][str(date)] = {
                "positive": 0, "negative": 0}

        # if the positive probability is more than the negative, it predicts negative
        if current_positive > current_negative:
            # number of positive predicitons for current company
            positive_predictions[row[1]] += 1
            # for line chart data
            sentiment_values[row[1]][str(date)]["positive"] += 1
        else:
            # number of negative predicitons for current company
            negative_predictions[row[1]] += 1
            sentiment_values[row[1]][str(date)]["negative"] += 1

    # loop through each company
    for company in company_names:
        # add the line chart data to the database
        dao.add_sentiment_values(
            company, positive_predictions[company], negative_predictions[company], json.dumps(sentiment_values[company]))


def test(test_tweets):
    """
    Runs Naive Bayes on a test set, for cross validation and building a confusion matrix.
        Parameters:
            test_tweets (list): List containing all test Tweets for the current fold
        Returns:
            Dictionary containing the confusion matrix and accuracy achieved for this fold.
    """
    num_correct = 0
    missing = 0

    confusion_matrix = {"true_positive": 0, "false_positive": 0,
                        "false_negative": 0, "true_negative": 0}

    # loop through each row in the test set and perform Naive Bayes
    for index, row in test_tweets.iterrows():
        current_positive = prior_probs["pos"]
        current_negative = prior_probs["neg"]

        if not isinstance(row['text'], str):
            missing += 1
            continue

        for word in row['text'].split(" "):
            laplace_smoothing(word)

            current_positive *= positive_probs[word]
            current_negative *= negative_probs[word]

        if current_positive > current_negative:
            sentiment = 2
        else:
            sentiment = -2

        if sentiment == row['target']:
            num_correct += 1  # increment number of correct predictions

            if sentiment == 2:
                confusion_matrix["true_positive"] += 1
            elif sentiment == -2:
                confusion_matrix["true_negative"] += 1
        else:
            if sentiment == 2:
                confusion_matrix["false_positive"] += 1
            elif sentiment == -2:
                confusion_matrix["false_negative"] += 1

    accuracy = num_correct / (len(test_tweets) - missing)  # calculate accuracy

    return {"confusion": confusion_matrix, "accuracy": accuracy}


def cross_valdation():
    """
    Cross validation for accuracy testing and confusion matrix calculations.
    Prints all results to the console.
    """

    # get the datasets for each fold of the cross validation
    folds = utility.get_fold_datasets()

    # initialise confusion matrix
    average_confusion = {"true_positive": 0, "false_positive": 0,
                         "false_negative": 0, "true_negative": 0}
    average_accuracy = 0

    # loop through each dataset for each fold
    for key, dataset in folds.items():

        # train the classifier on the training set for the current fold
        train(dataset["training"])
        # get the conditional probabilities for current fold
        calc_conditional_probabilities()
        # test the classifier on the test set for the current fold
        test_results = test(dataset['test'])

        # print accuracy results to console
        print(key + ":")
        print(test_results["confusion"])
        print(str(test_results["accuracy"] * 100) + "%")

        # calculate confusion matrix values for current fold
        average_confusion["true_positive"] += test_results["confusion"]["true_positive"] / \
            len(folds)
        average_confusion["false_positive"] += test_results["confusion"]["false_positive"] / \
            len(folds)
        average_confusion["true_negative"] += test_results["confusion"]["true_negative"] / \
            len(folds)
        average_confusion["false_negative"] += test_results["confusion"]["false_negative"] / \
            len(folds)

        # add current accuracy to average accuracy
        average_accuracy += test_results["accuracy"]

    # calculate average accuracy across 5 folds
    average_accuracy = average_accuracy / len(folds)

    # print 5-fold averages
    print()
    print("Averages after " + str(len(folds)) + " folds: ")
    print(average_confusion)
    print(str(average_accuracy * 100) + "%")
    print()


def run_scikit():
    """
    Runs 5-fold cross validation on Scikit-learn Multinomial Naive Bayes.
    This is used for accuracy comparisons against my implementation.
    """

    vectorizer = CountVectorizer()  # used for vectorizing the Tweets
    folds = utility.get_fold_datasets()  # get the datasets for each fold
    average_accuracy = 0

    # loop through each fold
    for key, dataset in folds.items():

        # get training tweets for current fold
        train_tweets = dataset["training"]

        # alpha 1.0 for Laplace smoothing
        nb = MultinomialNB(alpha=1.0, fit_prior=True)

        vectorizer.fit(train_tweets.text.astype('U'))  # vectorize training set
        train_array = vectorizer.transform(train_tweets.text.astype('U'))

        # fit the training set to the Naive Bayes classifier
        nb.fit(train_array, train_tweets.target)

        test_tweets = dataset["test"]  # get test tweets for current fold
        test_vector = vectorizer.transform(
            test_tweets.text.astype('U'))  # vectorize test set

        # make predictions on test set
        test_predicted = nb.predict(test_vector)

        # use metrics to get the current accuracy as a float
        current_accuracy = metrics.accuracy_score(
            test_tweets.target, test_predicted)

        average_accuracy += current_accuracy

        # print the current accuracy as a percentage
        print(key + ":")
        print("Scikit-learn: " + str(current_accuracy * 100) + "%")

    # print the average accuracy across the 5 folds as a percentage
    print()
    print("Scikit avg. : " + str((average_accuracy / len(folds)) * 100) + "%")


def get_word_clouds():
    """
    Gets data for the word clouds. Similar to run_naive_bayes(), needs more generalising. 
    Most of the parts in this function come from run_naive_bayes() so will not be commented on.
        Returns:
            bag_of_words(dictionary): The bag of words for positive and negative words.
    """

    dao = DAO()

    train(utility.get_train())

    calc_conditional_probabilities()

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

    bag_of_words = {"positive_train": {}, "negative_train": {},
                    "positive_unseen": {}, "negative_unseen": {}}

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

            # loop through each word in the current row
            for word in row[3].split(" "):
                if word == "climate" or word == "change" or word == "global":
                    continue

                if word not in bag_of_words["positive_unseen"].keys():
                    bag_of_words["positive_unseen"][word] = 0

                bag_of_words["positive_unseen"][word] += 1

        else:
            negative_predictions[row[1]] += 1
            for word in row[3].split(" "):
                if word == "climate" or word == "change" or word == "global":
                    continue

                if word not in bag_of_words["negative_unseen"].keys():
                    bag_of_words["negative_unseen"][word] = 0

                bag_of_words["negative_unseen"][word] += 1

    for word in sorted(positive_dict, key=positive_dict.get, reverse=True):
        if word == "climate" or word == "change" or word == "global":
            continue
        bag_of_words["positive_train"][word] = positive_dict[word]

    for word in sorted(negative_dict, key=negative_dict.get, reverse=True):
        if word == "climate" or word == "change" or word == "global":
            continue
        bag_of_words["negative_train"][word] = negative_dict[word]

    return bag_of_words

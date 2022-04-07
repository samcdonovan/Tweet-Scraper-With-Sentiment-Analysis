from string import digits
import string
import pandas as pd
import re
from nltk.corpus import stopwords  # Import stopwords from nltk.corpus
import csv  # Import the csv module to work with csv files
import nltk
import sys
import unicodedata
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
wordnet.ensure_loaded()
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')
# nltk.download('stopwords')


def get_stop_words():
    stop_list = []
    with open('data/stop_words.csv', 'r') as file:
        stop_list = file.read().strip().split(",")

    return stop_list


stop_words = get_stop_words()


def clean_and_lemmatize(text):
    wnl = WordNetLemmatizer()
    converted_tweet = convert_to_list(text)

    tagged = nltk.pos_tag(converted_tweet)
    wordnet_tagged = list(
        map(lambda x: (x[0], pos_tagger(x[1])), tagged))

    lemmatized_sentence = []
    for word, tag in wordnet_tagged:
        if tag is None:
            # if there is no available tag, append the token as is
            lemmatized_sentence.append(word)
        else:
            # else use the tag to lemmatize the token
            lemmatized_sentence.append(wnl.lemmatize(word, tag))

    cleaned_text = " ".join(lemmatized_sentence)
    return cleaned_text


def pos_tagger(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


def create_csv():

    stop_words = stopwords.words('english')
    with open('data/stop_words.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(stop_words)


def convert_to_list(sentence):
    converted_list = []

    sentence = ''.join(filter(lambda x: x in string.printable, sentence))

    re.sub('((www.[^s]+)|(https?://[^s]+))', ' ', sentence)
    english_punctuations = string.punctuation
    punctuations_list = english_punctuations

    remove_punctuation = str.maketrans('', '', punctuations_list)
    # re.sub('[0-9]+', '', sentence)
    remove_digits = str.maketrans('', '', digits)
    # sentence = sentence.translate(remove_digits)
    # sentence = sentence.translate(remove_punctuation)
    regex = re.compile('[@#]|((www.[^s]+)|(https?://[^s]+))')
    re.sub(r'[^\w]', '', sentence)

    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    emoji_pattern.sub(r'', sentence)

    for word in sentence.split():

        # print(regex.search(word))
        if regex.search(word) != None:
            continue

        word = word.lower()
        stop_check = bool(False)
        word = word.translate(remove_digits)
        word = word.translate(remove_punctuation)
        emoji_pattern.sub(r'', word)
        # print(word + " " + str(word in stop_words))
        word.replace(" ", "")
        if "http" in word or "htt" in word or len(word) < 3 or word in stop_words:
            stop_check = True
            # print(word)
            continue

        """
        for stop_word in stop_words:
            if word.lower() in stop_word:
                stop_check = bool(True)
        """
        # print(word + ";")
        if not word.isspace() and word:
            """
            word = word.translate(dict.fromkeys(i for i in range(sys.maxunicode)
                                                if unicodedata.category(chr(i)).startswith('P')))
            """

            converted_list.append(word)

    return converted_list


def tokenize(text):
    return text.split()


def get_train():

    dataframe = pd.read_csv('./data/training_set.csv', encoding='ISO-8859-1', compression=None)
    return dataframe


def get_test():
    dataframe = pd.read_csv('./data/test_set.csv', encoding='ISO-8859-1', compression=None)
    return dataframe


def training_and_test_to_csv():

    climate_dataframe = pd.read_csv('./data/sample_data.csv', encoding='ISO-8859-1', compression=None,
                                    names=['target', 'text', 'id'])

    climate_data = climate_dataframe[['text', 'target']]

    #training_data.loc[training_data['target'] == 0, 'target'] = 3
    #training_data.loc[training_data['target'] == 2, 'target'] = 3
    climate_data.loc[climate_data['target'] == 1, 'target'] = 2
    climate_data.loc[climate_data['target'] == -1, 'target'] = -2
    #training_data.loc[training_data['target'] == 3, 'target'] = 1

    climate_positive = climate_data[climate_data['target'] == 2]
    climate_negative = climate_data[climate_data['target'] == -2]
    #training_neutral = training_data[training_data['target'] == 1]

    training_positive = climate_positive.iloc[:int(10000)]
    training_negative = climate_negative.iloc[:int(10000)]

    test_positive = climate_positive.iloc[-int(2000):]
    test_negative = climate_negative.iloc[-int(2000):]
    #training_neutral = training_neutral.iloc[:int(2333)]

    climate_train = pd.concat([training_negative, training_positive])
    climate_test = pd.concat([test_negative, test_positive])


    """
    sentiment_140_dataframe = pd.read_csv('./data/sentiment_140_dataset.csv', encoding='ISO-8859-1', compression=None,
                                          names=['target', 'ids', 'date', 'flag', 'user', 'text'])

    sentiment_140_data = sentiment_140_dataframe[['text', 'target']]

    sentiment_140_data.loc[sentiment_140_data['target'] == 4, 'target'] = 2
    sentiment_140_data.loc[sentiment_140_data['target'] == 0, 'target'] = -2

    sentiment_140_positive = sentiment_140_data[sentiment_140_data['target'] == 2]
    sentiment_140_negative = sentiment_140_data[sentiment_140_data['target'] == -2]

    training_positive = sentiment_140_positive.iloc[:int(6750)]
    training_negative = sentiment_140_negative.iloc[:int(6750)]

    test_positive = sentiment_140_positive.iloc[-int(2000):]
    test_negative = sentiment_140_negative.iloc[-int(2000):]

    sentiment_140_train = pd.concat([training_negative, training_positive])
    sentiment_140_test = pd.concat([test_negative, test_positive])
    """
    #    training_set = pd.concat([climate_train, sentiment_140_train])
    #   test_set = pd.concat([climate_test, sentiment_140_test])

    training_set = climate_train
    test_set = climate_test
    for index, row in training_set.iterrows():

        training_set.loc[index, 'text'] = clean_and_lemmatize(row['text'])

    for index, row in test_set.iterrows():

        test_set.loc[index, 'text'] = clean_and_lemmatize(row['text'])

    try:

        training_set.to_csv('./data/training_set.csv', index=False)
        test_set.to_csv('./data/test_set.csv', index=False)
    except Exception as ex:
        print("Training data error: " + str(ex))


def get_training_data_climate():

    df = pd.read_csv('./data/sample_data.csv', encoding='ISO-8859-1', compression=None,
                     names=['target', 'text', 'id'])

    training_data = df[['text', 'target']]

    #training_data.loc[training_data['target'] == 0, 'target'] = 3
    #training_data.loc[training_data['target'] == 2, 'target'] = 3
    training_data.loc[training_data['target'] == 1, 'target'] = 2
    training_data.loc[training_data['target'] == -1, 'target'] = -2
    #training_data.loc[training_data['target'] == 3, 'target'] = 1

    training_positive = training_data[training_data['target'] == 2]
    training_negative = training_data[training_data['target'] == -2]
    #training_neutral = training_data[training_data['target'] == 1]

    training_positive = training_positive.iloc[:int(3500)]
    training_negative = training_negative.iloc[:int(3500)]
    #training_neutral = training_neutral.iloc[:int(2333)]

    training_set = pd.concat([training_negative, training_positive])

    for index, row in training_set.iterrows():

        training_set.loc[index, 'text'] = clean_and_lemmatize(row['text'])

    try:

        training_set.to_csv('./data/training_set_2.csv', index=False)
    except Exception as ex:
        print("Training data error: " + str(ex))


def get_training_data_140():
    df = pd.read_csv('./data/sample_data.csv', encoding='ISO-8859-1', compression=None,
                     names=['target', 'ids', 'date', 'flag', 'user', 'text'])

    training_data = df[['text', 'target']]

    training_data.loc[training_data['target'] == 4, 'target'] = 2
    training_data.loc[training_data['target'] == 0, 'target'] = -2

    training_positive = training_data[training_data['target'] == 2]
    training_negative = training_data[training_data['target'] == -2]

    training_positive = training_positive.iloc[:int(3500)]
    training_negative = training_negative.iloc[:int(3500)]

    training_set = pd.concat([training_negative, training_positive])

    for index, row in training_set.iterrows():

        training_set.loc[index, 'text'] = clean_and_lemmatize(row['text'])

    try:

        training_set.to_csv('./data/training_set.csv', index=False)
    except Exception as ex:
        print("Training data error: " + ex)


def sum(array):
    sum = 0

    for i in range(len(array)):
        sum += array[i]

    return sum

def isNaN(number):
    return number != number
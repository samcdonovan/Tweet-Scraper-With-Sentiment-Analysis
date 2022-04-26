from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly
import chart_studio as py
from string import digits
import string
import pandas as pd
import naive_bayes
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import json
import re
from nltk.corpus import stopwords  # Import stopwords from nltk.corpus
import csv  # Import the csv module to work with csv files
import nltk
import sys
import unicodedata
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from regex import P
from data_access_object import DAO
wordnet.ensure_loaded()
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')

chart_colours =['rgb(60,179,113)', 'rgb(255,69,0)'] # global variable for positve and negative colours

# set Plotly account credentials
py.tools.set_credentials_file(
    username='samcdonovan', api_key='KeNXeNkDds8Ns0b85fni')


def plot_word_clouds():
    """
    Plots two word clouds for the most common words in the positive and negative bags of words. Uses the WordCloud library.
    """

    word_cloud = naive_bayes.get_word_clouds()

    wordcloud = WordCloud()

    # generates word clouds for each set of words
    wordcloud.generate_from_frequencies(frequencies=word_cloud["positive_unseen"])
    wordcloud.generate_from_frequencies(frequencies=word_cloud["negative_unseen"])

    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def plot_pie_charts():
    """
    Plots pie charts of positive and negative distribution of Tweets for each company using Plotly.
    """

    sentiment_values = DAO().get_sentiment_values() # get values from MySQL database
    labels = ["Positive", "Negative"]

    pie_chart = make_subplots(rows=2, cols=3, specs=[[{'type': 'domain'}, {
        'type': 'domain'},  {'type': 'domain'}], [{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]])

    # add traces for each company
    pie_chart.add_trace(go.Pie(labels=labels, values=[sentiment_values[2][1], sentiment_values[2][2]], name=sentiment_values[2][0], marker_colors=chart_colours),
                        1, 1)
    pie_chart.add_trace(go.Pie(labels=labels, values=[sentiment_values[1][1], sentiment_values[1][2]], name=sentiment_values[1][0]),
                        1, 2)
    pie_chart.add_trace(go.Pie(labels=labels, values=[sentiment_values[0][1], sentiment_values[0][2]], name=sentiment_values[0][0]),
                        1, 3)
    pie_chart.add_trace(go.Pie(labels=labels, values=[sentiment_values[4][1], sentiment_values[4][2]], name=sentiment_values[4][0]),
                        2, 1)
    pie_chart.add_trace(go.Pie(labels=labels, values=[sentiment_values[3][1], sentiment_values[3][2]], name=sentiment_values[3][0]),
                        2, 2)

    # get total number of negative Tweets
    total_negative = sentiment_values[1][1] + sentiment_values[0][1] + \
        sentiment_values[3][1] + \
        sentiment_values[2][1] + sentiment_values[4][1]

    # get total number of positive Tweets
    total_positive = sentiment_values[1][2] + sentiment_values[0][2] + \
        sentiment_values[3][2] + \
        sentiment_values[2][2] + sentiment_values[4][2]

    # add pie chart for total polarity distribution
    pie_chart.add_trace(go.Pie(labels=labels, values=[total_negative, total_positive], name="Total"),
                        2, 3)
    pie_chart.update_traces(hoverinfo="label+percent+name", textfont_size=20,
                            textinfo="percent+value", marker=dict(line=dict(color='#000000', width=1)))

    pie_chart.update_layout(
        title_text="<b>F.A.A.N.G companies' Twitter sentiment</b>",
        title_x=0.5,
        title_font_size=30,
        title_font_family='Arial',

        annotations=[dict(text='<b>Facebook</b>', x=0.125, y=1.05, font_size=11, showarrow=False),
                     dict(text='<b>Apple</b>', x=0.5, y=1.05,
                          font_size=12, showarrow=False),
                     dict(text='<b>Amazon</b>', x=0.885, y=1.05,
                          font_size=12, showarrow=False),
                     dict(text='<b>Netflix</b>', x=0.125, y=0.45,
                          font_size=12, showarrow=False),
                     dict(text='<b>Google</b>', x=0.5, y=0.45,
                          font_size=12, showarrow=False),
                     dict(text='<b>All Tweets</b>', x=0.885, y=0.45, font_size=12, showarrow=False)])

    pie_chart.show()


def plot_line_chart():

    sentiment_values = DAO().get_sentiment_values()
    positive = {}
    negative = {}
    labels = ["Positive", "Negative"]

    totals = {"positive":{}, "negative": {}}
    for index in range(0, 5):
      

        json_sentiment = eval(sentiment_values[index][3])
        positive = {}
        negative = {}
        for key in json_sentiment.keys():
            if key not in totals["positive"].keys():

                totals["positive"][key] = 0
                totals["negative"][key] = 0

            totals["positive"][key] += json_sentiment[key]["positive"]
            totals["negative"][key] += json_sentiment[key]["negative"]

            positive[key] = json_sentiment[key]["positive"]
            negative[key] = json_sentiment[key]["negative"]

        draw_line_chart(sentiment_values[index][0].capitalize(), positive, negative)

    draw_line_chart("All Tweets", totals["positive"], totals["negative"])

def draw_line_chart(name, positive, negative):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(positive.keys()), y=list(positive.values()),
                                mode='lines+markers',
                                name='Positive',
                                line=dict(color=chart_colours[0])))
    fig.add_trace(go.Scatter(x=list(negative.keys()), y=list(negative.values()),
                                mode='lines+markers',
                                name='Negative',
                                line=dict(color=chart_colours[1])))

    fig.update_xaxes(
        tickangle=90,
        title_text="Date",
        title_font={
            "size": 20,
            "family": 'Arial'
        },
        title_standoff=25,
        dtick =86400000.0 
    )

    fig.update_yaxes(
        title_text="Number of Tweets",
        title_standoff=25,
        title_font={
            "size": 20,
            "family": 'Arial'
        },
    )

    fig.update_layout(
        title_text="<b>" + name + "'s Tweet sentiment over time</b>",
        title_x=0.5,
        title_font_size=30,
        title_font_family='Arial',
        xaxis_range = [ list(positive.keys())[0], list(positive.keys())[-1]],
        width=800, height=400
    )
    fig.show()


def get_stop_words():
    """
    Gets all stop words from local file and puts them into a list.
        Returns:
            stop_list (string[]): List containing all stop words.
    """

    stop_list = []
    with open('data/stop_words.csv', 'r') as file:
        stop_list = file.read().strip().split(",")

    return stop_list

stop_words = get_stop_words() # put all stop words into global variable

def print_stop_words():
    for word in stop_words:
        print(word)

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

    remove_digits = str.maketrans('', '', digits)
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

        if regex.search(word) != None:
            continue

        word = word.lower()
        word = word.translate(remove_digits)
        word = word.translate(remove_punctuation)
        emoji_pattern.sub(r'', word)
        word.replace(" ", "")
        if "http" in word or "htt" in word or len(word) < 3 or word in stop_words:
             continue
 
        if not word.isspace() and word:
            converted_list.append(word)

    return converted_list


def tokenize(text):
    return text.split()


def get_train():

    dataframe = pd.read_csv('./data/training_set.csv',
                            encoding='ISO-8859-1', compression=None)
    return dataframe


def get_test():
    dataframe = pd.read_csv('./data/test_set.csv',
                            encoding='ISO-8859-1', compression=None)
    return dataframe


def training_csv():

    climate_dataframe = pd.read_csv('./data/sample_data.csv', encoding='ISO-8859-1', compression=None,
                                    names=['target', 'text', 'id'])

    climate_data = climate_dataframe[['text', 'target']]

    climate_data.loc[climate_data['target'] == 1, 'target'] = 2
    climate_data.loc[climate_data['target'] == -1, 'target'] = -2

    climate_positive = climate_data[climate_data['target'] == 2]
    climate_negative = climate_data[climate_data['target'] == -2]
    training_positive = climate_positive.iloc[-int(12000):]
    #training_positive = pd.concat([climate_positive.iloc[:int(8500)], climate_positive.iloc[-int(8500):]])
    #test_positive = climate_positive.iloc[-int(5000):]

    sentiment_140_dataframe = pd.read_csv('./data/sentiment_140_dataset.csv', encoding='ISO-8859-1', compression=None,
                                          names=['target', 'ids', 'date', 'flag', 'user', 'text'])

    sentiment_140_data = sentiment_140_dataframe[['text', 'target']]
    sentiment_140_data.loc[sentiment_140_data['target'] == 0, 'target'] = -2

    sentiment_140_negative = sentiment_140_data[sentiment_140_data['target'] == -2]

  #  training_negative = pd.concat([climate_negative.iloc[:int(4000)], sentiment_140_negative.iloc[:int(6500)],
    #              sentiment_140_negative.iloc[-int(6500):]])
    training_negative = pd.concat([climate_negative.iloc[:int(4000)],
                                  sentiment_140_negative.iloc[-int(8000):]])
    #test_negative = sentiment_140_negative.iloc[-int(5000):]

    climate_train = pd.concat([training_negative, training_positive])
    """
    climate_test = pd.concat([test_negative, test_positive])

    training_set = climate_train
    test_set = climate_test
    dataset = pd.concat([training_set, test_set])
    """
    dataset = climate_train

    for index, row in dataset.iterrows():

        dataset.loc[index, 'text'] = clean_and_lemmatize(row['text'])

    try:
        dataset.to_csv('./data/training_data.csv', index=False)

    except Exception as ex:
        print("Training data error: " + str(ex))


def get_fold_datasets():
    dataframe = pd.read_csv('./data/training_data.csv',
                            encoding='ISO-8859-1', compression=None)

    dataframe = dataframe.sample(frac=1)
    positive_set = dataframe[dataframe['target'] == 2]
    negative_set = dataframe[dataframe['target'] == -2]

    fold_data = {}
    for index in range(0, 5):
        fold_name = "fold-" + str(index)
        fold_data[fold_name] = {}

        start_index = index * 2000
        end_index = start_index + 3000
        # print(start_index)
        # print(end_index)
        # print(len(positive_set))
        training_positive = pd.concat(
            [positive_set.iloc[0:start_index], positive_set.iloc[(end_index+1):]])

        training_negative = pd.concat(
            [negative_set.iloc[0:start_index], negative_set.iloc[(end_index+1):]])
        #print(positive_set.iloc[start_index + 1:end_index])
        # print(positive_set.iloc[20000:25000])
        training_set = pd.concat([training_positive, training_negative])
        # print(training_set)
        test_set = pd.concat([positive_set.iloc[(start_index + 1):end_index],
                              negative_set.iloc[(start_index + 1):end_index]])
        # print(test_set)
        fold_data[fold_name]["training"] = training_set
        fold_data[fold_name]["test"] = test_set

    return fold_data
   # print(fold_data)


def training_and_test_to_csv():

    climate_dataframe = pd.read_csv('./data/sample_data.csv', encoding='ISO-8859-1', compression=None,
                                    names=['target', 'text', 'id'])

    climate_data = climate_dataframe[['text', 'target']]
    climate_data.loc[climate_data['target'] == 1, 'target'] = 2
    climate_data.loc[climate_data['target'] == -1, 'target'] = -2

    climate_positive = climate_data[climate_data['target'] == 2]
    climate_negative = climate_data[climate_data['target'] == -2]

    sentiment_140_dataframe = pd.read_csv('./data/sentiment_140_dataset.csv', encoding='ISO-8859-1', compression=None,
                                          names=['target', 'ids', 'date', 'flag', 'user', 'text'])

    sentiment_140_data = sentiment_140_dataframe[['text', 'target']]
    sentiment_140_data.loc[sentiment_140_data['target'] == 0, 'target'] = -2

    training_positive = climate_positive.iloc[:int(8000)]

    test_positive = climate_positive.iloc[-int(5000):]

    sentiment_140_negative = sentiment_140_data[sentiment_140_data['target'] == -2]

    training_negative = pd.concat([climate_negative.iloc[:int(4000)],
                                  sentiment_140_negative.iloc[:int(4000)]])

    test_negative = sentiment_140_negative.iloc[-int(5000):]

    climate_train = pd.concat([training_negative, training_positive])
    climate_test = pd.concat([test_negative, test_positive])

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


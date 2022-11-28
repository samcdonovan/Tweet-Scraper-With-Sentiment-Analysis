<h1 align="center">Tweet Sentiment Analysis Project</h1>

<div align="center">

  [![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

## 📝 Table of Contents
- [About](#about)
- [Libraries/Frameworks/Services](#built_using)
- [Authors](#authors)

## ℹ️ About <a name = "about"></a>
Climate change is an ever-present issue and widely discussed amongst the population. With the drastic effects of climate change at our doorstep, many people are using social media to voice their opinion and engage in debate. Large organisations such as the F.A.A.N.G companies play a critical role in climate change, and therefore many climate-conscious consumers look towards these companies to help make changes to their climate impact. Sentiment analysis is a widely used and researched topic in Computer Science; this project aims to further explore the use of sentiment analysis techniques. In this project, it was implemented to analyse “Tweets” about F.A.A.NG companies in relation to climate change from the social media platform, Twitter (Tweets were collected using the Twitter API). 

The sentiment analysis technique used in this project is a Multinomial Naïve Bayes classifier which, in this implementation, predicts whether a given Tweet is positive or negative. To evaluate this implementation, a 5-fold cross validation test was run, measuring at 87.75% average accuracy. This demonstrates how effective Naïve Bayes can be whilst retaining implementation simplicity. The results were then analysed to make inferences on the public’s opinion about each F.A.A.N.G company in relation to climate change. It was found that Facebook had the most positive Tweets with 56.7% being positive, Amazon on the other hand had the most negative with 63.8%. Apple, Netflix, and Google resulted in a close to even distribution of positive/negative Tweets (leaning towards negative). This suggests the public views Facebook as a more positive company in relation to climate change, and the other companies as more negative. The results also demonstrate other implications, most notably that the date/time this data was collected likely heavily influences the public’s opinion of a company at any given time. Further analysis could be performed using a wider range of companies, and with a focus on exploring sentiment over a larger timescale. This would shed light on time periods where discussion around these topics is at a peak (e.g., during ongoing major events) which could influence how the public view these companies and demonstrate further implications on their climate impact. 


## 💻 Libraries/Frameworks/Modules <a name = "built_using"></a>
## Python
- [Tweepy](https://www.tweepy.org/): Twitter API library, used to scrape Tweets about the F.A.A.N.G companies and climate change.
-	[Datetime](https://docs.python.org/3/library/datetime.html): Time and date data types; for retrieving Tweets from different dates
- [Threading](https://docs.python.org/3/library/threading.html): Thread-based parallelism; for creating threads to run the four different scrapers
-	[MySQL connector](https://dev.mysql.com/doc/connector-python/en/): Connector for MySQL database
- [CSV](https://docs.python.org/3/library/csv.html): Handles CSV files for storing and retrieving data
-	[NLTK](https://www.nltk.org/): Natural Language Toolkit; provided lemmatization functionality
-	[Scikit-learn](https://scikit-learn.org/stable/): Machine Learning library; used for comparing Naïve Bayes algorithm against the implementation in this project 
-	[Pandas](https://pandas.pydata.org/): Data analysis library; used for creating and handling ‘dataframes’ which allowed for dataset manipulation (chiefly for creating training and test datasets)
-	[Plotly](https://plotly.com/python/) and [WordCloud](https://pypi.org/project/wordcloud/): Data visualization libraries; used for creating charts for representing the results of the accuracy tests and sentiment analysis


## ✍️ Authors <a name = "authors"></a>
- [@samcdonovan](https://github.com/samcdonovan)

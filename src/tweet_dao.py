
from re import S
import pandas
import os
import time
import xlsxwriter
import openpyxl
from openpyxl.styles import Font
import sqlalchemy as sal
from mysql.connector import errorcode
from sqlalchemy import create_engine
import datetime

import mysql.connector

class TweetDAO():

  def init_db(self):
    self.new_connection()

  def new_connection(self):
    try:
      self.connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database='scraped_tweets'
      )

      #self.cursor = self.connection.cursor()

    except mysql.connector.Error as error:
      if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Username or password does not match.")
      elif error.errno == errorcode.ER_BAD_DB_ERROR:
        print("Cannot locate database.")
      else:
        print("Database error: ")
        print(error)

  def set_cursor(self, cursor):
    self.cursor = cursor

  def get_tweet_id_with_date(self, min_or_max, current_date, company_name):
    previous_date = current_date - datetime.timedelta(1)
    query = "SELECT " + min_or_max + "(id) FROM tweets WHERE company='" + company_name + "' AND timestamp BETWEEN '%s' and '%s'" % (previous_date, current_date)
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database='scraped_tweets'
    )
    cursor = connection.cursor(buffered = True)
    cursor.execute(query)
    tweet_id = cursor.fetchone()
    if tweet_id is None:
      tweet_id = 0
    print(tweet_id)

    cursor.close()
    connection.close()
    return tweet_id

  def get_newest_tweet(self, company_name):
    query = "SELECT MAX(id), MAX(timestamp) FROM tweets WHERE timestamp = (SELECT MAX(timestamp) FROM tweets WHERE company='" + company_name + "')" 
   
    #self.connection.reconnect()
    #self.new_connection()
    #self.cursor.close()
    #self.connection.close()
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database='scraped_tweets'
      )
    cursor = connection.cursor(buffered = True)
 
    try:
       # print("m")
        time.sleep(2)
       # print("d")
        #try:
        #print(cursor)
        cursor.execute(query)
       # except Exception as error:
          #print("error: " + str(error))
        #print("s")
        #self.connection.commit()
        #print("y")
        tweet = cursor.fetchone()
       # print(tweet)
        cursor.close()
        connection.close()
        return tweet
    except mysql.connector.Error as error:
        print("SQL database error: " + str(error))
        cursor.close()
        connection.close()
        return None
        #sys.exit(1)
    
   # return self.cursor.fetchone()

  def get_tweet_id(self, min_or_max):
    query = "SELECT " + min_or_max + "(id) FROM tweets"
    self.cursor.execute(query)

    return self.cursor.fetchone()

  def add_to_database(self, tweet):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database='scraped_tweets'
      )
    cursor = connection.cursor(buffered = True)
    check_unique = "SELECT * FROM tweets WHERE id = " + str(tweet.unique_id)
    cursor.execute(check_unique)

    check_result = cursor.fetchall()

    if len(check_result) > 0:
      print("Tweet with ID " + str(tweet.unique_id) + " already exists in the database.")
      return None

    add_tweet = ("INSERT INTO tweets "
                "(id, company, original_tweet, cleaned_tweet, timestamp)"
                "VALUES (%s, %s, %s, %s, %s)")
    tweet_data = (tweet.unique_id, tweet.company, tweet.original_tweet, tweet.cleaned_text, tweet.time)

    cursor.execute(add_tweet, tweet_data) 

    connection.commit()
    cursor.close()
    connection.close()

  def close_connection(self):
  
    self.cursor.close()
    self.connection.close()
    print("Database connection closed.")
 
  def init_db_excel(self):
    #print(os.path.abspath(os.curdir))
   # print(os.chdir(".."))
    
    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_name = "scraped_tweets.csv"
    full_path = os.path.abspath(os.curdir) + os.path.sep + "data" + os.path.sep + file_name
    
   # print(full_path)
   
    if not os.path.isfile(full_path):
       # writer = pandas.ExcelWriter(full_path, engine = 'xlsxwriter')
        initial_file = pandas.DataFrame(columns=['Company', 'Original Tweet', 'Cleaned Tweet', 'Timestamp'])
        #initial_file['A1'].font = Font(bold=True)
        #initial_file.style.applymap("font-weight: bold", subset=)
       # writer.save()
       # workbook = openpyxl.load_workbook(full_path)
       # worksheet = workbook.active
       # worksheet['A1'] = "ID"
       # worksheet['A1'].font = Font(bold=True)

      #  worksheet['B1'] = "Company"
      #  worksheet['B1'].font = Font(bold=True)
        
        #worksheet['C1'] = "Original Tweet"
        #worksheet['C1'].font = Font(bold=True)
        
       # worksheet['D1'] = "Cleaned Tweet"
       # worksheet['D1'].font = Font(bold=True)
        
        #worksheet['E1'] = "Date and time"
        #worksheet['E1'].font = Font(bold=True)
        
        #initial_file.index.name = 'ID'
        #worksheet.cell(column=1, row=1, value="id").font
        initial_file.to_csv(os.path.abspath(os.curdir) + os.path.sep + "data" + os.path.sep + "scraped_tweets.csv",encoding='utf-8', index=False)
        #workbook.save(os.path.abspath(os.curdir) + os.path.sep + "data" + os.path.sep + "scraped_tweets.csv")
        self.database_df = initial_file
        #excel_doc = pandas.read_excel(full_path, engine = 'openpyxl')
        #excel_doc.to_excel(writer, sheet_name='Sheet1', index = False)
      #  writer.save()
    else:
        self.database_df = pandas.read_csv(os.path.abspath(os.curdir) + os.path.sep + "data" + os.path.sep + "scraped_tweets.csv", index_col=False)
        print(self.database_df)
        #print(self.database_df.size)
    #engine = create_engine('mysql+pymysql://root:''@127.0.0.1/scraped_tweets') 
    #print(engine.table_names())

  def add_to_database_excel(self, tweet):
   # print(tweet.company)
   # new_row = pandas.DataFrame(columns=[)
    #self.database_df.loc[self.database_df.size + 1] = [tweet.company, tweet.original_tweet, tweet.cleaned_text, tweet.time] 
    #self.database_df.index.name = 'ID'
    new_entry = { 'Company': tweet.company, 'Original Tweet' : tweet.original_tweet, 'Cleaned Tweet': tweet.cleaned_text, "Timestamp": tweet.time}
    self.database_df.loc[self.database_df.size + 1] = new_entry
    #'ID': self.database_df.size + 1,
    #
    
    #initial_file.index.name = 'ID'
    #self.database_df = self.database_df.append(new_entry, ignore_index=False)
    print(self.database_df)

  def save_and_close_database_excel(self):
    #print(self.database_df)
    self.database_df.to_csv(os.path.abspath(os.curdir) + os.path.sep + "data" + os.path.sep + "scraped_tweets.csv", mode='a', header=False)
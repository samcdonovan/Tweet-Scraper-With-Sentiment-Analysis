
from re import S
import pandas
import os
import xlsxwriter
import openpyxl
from openpyxl.styles import Font
import sqlalchemy as sal
from mysql.connector import errorcode
from sqlalchemy import create_engine

import mysql.connector

class TweetDAO():

  def init_db(self):
    try:
      self.sql_db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database='scraped_tweets'
      )

      self.cursor = self.sql_db.cursor()

    except mysql.connector.Error as error:
      if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Username or password do not match.")
      elif error.errno == errorcode.ER_BAD_DB_ERROR:
        print("Cannot locate database.")
      else:
        print(error)

  def add_to_database(self, tweet):

   
    add_tweet = ("INSERT INTO tweets "
                "(company, original_tweet, cleaned_tweet, timestamp)"
                "VALUES (%s, %s, %s, %s)")
    tweet_data = (tweet.company, tweet.original_tweet, tweet.cleaned_text, tweet.time)

    self.cursor.execute(add_tweet, tweet_data) 

    self.sql_db.commit()
    
  def close_connection(self):
    self.cursor.close()
    self.sql_db.close()
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

import pandas
import os
import xlsxwriter
import openpyxl
#import sqlalchemy as sal

#from sqlalchemy import create_engine

#import mysql.connector
#mydb = mysql.connector.connect(
 # host="localhost",
  #user="root",
  #password=""
#)

#print(mydb)
class TweetDAO():

  def init_db(self):
    #print(os.path.abspath(os.curdir))
   # print(os.chdir(".."))
    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_name = "scraped_tweets.xlsx"
    full_path = os.path.abspath(os.curdir) + os.path.sep + "data" + os.path.sep + file_name
    
   # print(full_path)
    
    if not os.path.isfile(full_path):
        writer = pandas.ExcelWriter(full_path, engine = 'xlsxwriter')
        writer.save()
      
        #excel_doc = pandas.read_excel(full_path, engine = 'openpyxl')
        #excel_doc.to_excel(writer, sheet_name='Sheet1', index = False)
      #  writer.save()
    #engine = create_engine('mysql+pymysql://root:''@127.0.0.1/scraped_tweets') 
    #print(engine.table_names())


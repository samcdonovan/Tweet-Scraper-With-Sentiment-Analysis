
import pandas
import os
import xlsxwriter
import openpyxl
from openpyxl.styles import Font
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
       # writer = pandas.ExcelWriter(full_path, engine = 'xlsxwriter')
        initial_file = pandas.DataFrame(columns=['ID', 'Company', 'Original Tweet', 'Cleaned Tweet', 'Date and time'])
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
        
        #worksheet.cell(column=1, row=1, value="id").font
        initial_file.to_csv(os.path.abspath(os.curdir) + os.path.sep + "data" + os.path.sep + "scraped_tweets.csv",encoding='utf-8', index=False)
        #workbook.save(os.path.abspath(os.curdir) + os.path.sep + "data" + os.path.sep + "scraped_tweets.csv")
      
        #excel_doc = pandas.read_excel(full_path, engine = 'openpyxl')
        #excel_doc.to_excel(writer, sheet_name='Sheet1', index = False)
      #  writer.save()
    #engine = create_engine('mysql+pymysql://root:''@127.0.0.1/scraped_tweets') 
    #print(engine.table_names())

 # def add_to_database(tweet):

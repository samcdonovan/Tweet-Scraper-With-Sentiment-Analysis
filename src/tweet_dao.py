
import sqlalchemy as sal
from sqlalchemy import create_engine

import mysql.connector
#mydb = mysql.connector.connect(
 # host="localhost",
  #user="root",
  #password=""
#)

#print(mydb)
class TweetDAO():

  def init_db():
      #engine = sal.create_engine("mysql://user:root@localhost/scraped_tweets?charset=utf8mb4")
      engine = create_engine('mysql+pymysql://root:''@127.0.0.1/scraped_tweets') 
      #engine = sal.create_engine(‘mssql+pyodbc://local_host/scraped_tweets?driver=SQL Server?Trusted_Connection=yes’)
      print(engine.table_names())


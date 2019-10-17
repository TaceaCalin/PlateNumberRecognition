import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="CalinTacea",
  passwd="babolat",
  database="intelligentparking"
)

mycursor = mydb.cursor()

sql = "DROP DATABASE intelligentparking"

mycursor.execute(sql)

mydb.commit()
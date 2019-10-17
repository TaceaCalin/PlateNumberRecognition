import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="CalinTacea",passwd="babolat")
mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IntelligentParking")
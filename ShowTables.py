import mysql.connector

mydb = mysql.connector.connect(
            host="localhost",
            user="CalinTacea",
            passwd="babolat",
            database="intelligentparking"
        )

mycursor = mydb.cursor()

mycursor.execute("SHOW TABLES")

for x in mycursor:
    print(x)

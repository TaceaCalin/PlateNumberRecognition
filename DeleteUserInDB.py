import mysql.connector

mydb = mysql.connector.connect(
            host="localhost",
            user="CalinTacea",
            passwd="babolat",
            database="intelligentparking"
        )

mycursor = mydb.cursor()

mySql_delete_query = """DELETE from parking"""

mycursor.execute(mySql_delete_query)
mydb.commit()

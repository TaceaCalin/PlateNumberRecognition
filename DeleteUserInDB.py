import mysql.connector

mydb = mysql.connector.connect(
            host="localhost",
            user="CalinTacea",
            passwd="babolat",
            database="intelligentparking"
        )

mycursor = mydb.cursor()

mySql_delete_query = """DELETE from parking"""
mySql_reset_query = "alter table Parking auto_increment = 1"
mycursor.execute(mySql_delete_query)
mycursor.execute(mySql_reset_query)
mydb.commit()

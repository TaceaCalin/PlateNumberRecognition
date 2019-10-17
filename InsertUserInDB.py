import mysql.connector


def InsertUserInDB(name, platenumber, hours):
    mydb = mysql.connector.connect(
                host="localhost",
                user="CalinTacea",
                passwd="babolat",
                database="intelligentparking"
            )

    mycursor = mydb.cursor()

    mySql_insert_query = """INSERT INTO Parking (Name, PlateNumber,Hours) 
                               VALUES 
                               (%s,%s,%s) """
    recordTuple = (name, platenumber, hours)
    mycursor.execute(mySql_insert_query, recordTuple)
    mydb.commit()

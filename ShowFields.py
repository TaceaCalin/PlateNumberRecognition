import mysql.connector

mydb = mysql.connector.connect(
            host="localhost",
            user="CalinTacea",
            passwd="babolat",
            database="intelligentparking"
        )

mycursor = mydb.cursor()
try:
    mycursor.execute("SELECT * FROM Parking")
    results = mycursor.fetchall()
    print(results)
    for row in results:
        id = row[0]
        name = row[1]
        plateNumber = row[2]
        hours = row[3]

        # Now print fetched result
except:
    print("Error: unable to fecth data")

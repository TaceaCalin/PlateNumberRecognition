import mysql.connector

mydb = mysql.connector.connect(
            host="localhost",
            user="CalinTacea",
            passwd="babolat",
            database="intelligentparking"
        )

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE Parking (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), PlateNumber VARCHAR(255), Hours VARCHAR(255))")

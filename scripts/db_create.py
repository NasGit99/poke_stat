import mysql.connector
import sys
import os
from flask_mysqldb import MySQL


parent_directory = os.path.abspath('../')
sys.path.append(parent_directory)

from var import *

def create_database():
    mydb = mysql.connector.connect(
    host= host,
    user=db_user,
    password=db_password
    )

    mycursor = mydb.cursor()

    mycursor.execute("CREATE DATABASE PokeData")

    print('Database has been created')

if __name__ == "__main__":
    create_database()

import sys
import os
from flask_mysqldb import MySQL


parent_directory = os.path.abspath('../')
sys.path.append(parent_directory)
from var import *





def db_connection():
    import mysql.connector

    mydb = mysql.connector.connect(
    host=host,
    database = 'PokeData',
    user=db_user,
    password=db_password
    )

    return mydb
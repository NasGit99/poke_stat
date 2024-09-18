from pokemon_dex import sort_through_dex, insert_into_dex
from var import *
import pandas as pd
from sqlalchemy import create_engine
from db_connector import db_connection

def create_poke_database():

    mydb = db_connection()
    
    mycursor = mydb.cursor()

    mycursor.execute("CREATE DATABASE IF NOT EXISTS PokeData")

    print("Database is created")

    mycursor.execute("""
    
    use PokeData;
    
    CREATE TABLE IF NOT EXISTS poke_stats(
        id int,
        poke_name VARCHAR(75),
        type VARCHAR(25),
        type_2 VARCHAR(25),
        ability VARCHAR(25),
        ability_2 VARCHAR(25),
        hp INT,
        attack INT,    
        defense INT,               
        spatk INT,
        spdef INT,
        speed INT,
        PRIMARY KEY(id)
        ); 
    """)

    print("Table has been created")

    
def poke_dataframe():
    poke_col=['id','poke_name','type', 'type_2', 'ability', 'ability_2', 'hp',
              'attack', 'defense', 'spatk', 'spdef', 'speed']
    poke_data = insert_into_dex()
    poke_df = pd.DataFrame(poke_data, columns=poke_col)

    return poke_df

def insert_into_table():

    final_poke_df = poke_dataframe()

    engine = create_engine(f"mysql+mysqlconnector://{db_user}:{db_password}@localhost/PokeData")

    final_poke_df.to_sql('poke_stats', con=engine, if_exists='append', index=False)

    print("Data Inserted")
    
if __name__ == "__main__":

    create_poke_database()
    insert_into_table()

    print("Pokemon have been inserted into the database")


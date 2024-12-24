from db_connector import *
#Will move imports to a different file to reduce repetitiveness
import pandas as pd
import requests
import sqlite3 
from sqlalchemy import create_engine
from datetime import datetime
from var import *
import json


def get_machine_move(x):
        while True:
            api_url = f"https://pokeapi.co/api/v2/machine/{x}"
            response = requests.get(api_url)
            if response.status_code != 200:
                print("Tm or Hm is not valid")
                return None
            elif response.status_code == 200:
                data = response.json()
                break

        return data

def find_machine_data():
    machine_list ={
        "id":[],
        "machine_name":[],
        "move_name":[],
        "game_name":[]   
    }

    machine_counter = 1

    while True:
        try:
            
            selected_machine = get_machine_move(machine_counter)

            
            machine_id = selected_machine['id']
            machine_name = selected_machine['item']['name']
            move_name = selected_machine['move']['name']
            game_name = selected_machine['version_group']['name']

            #Insert data into dictionary

            machine_list['id'].append(machine_id)
            machine_list['machine_name'].append(machine_name)
            machine_list['move_name'].append(move_name)
            machine_list['game_name'].append(game_name)
            
            if machine_counter % 50 == 0:
                print(machine_name, 'appended')

            machine_counter += 1

        except Exception as e:
            # If any error occurs, print the error and break the loop
                print(f"Error processing move: {e}")
                break

    return machine_list

def create_tm_table():
     mydb = db_connection()
    
     mycursor = mydb.cursor()

     mycursor.execute(
    """
     CREATE TABLE IF NOT EXISTS machine_moves(    
        id big int,
        machine_name varchar(100),
        move_name varchar(100),
        game_name varchar(100)          

    );
        """)

def insert_into_machine_table():

    machine_data = find_machine_data()
    
    machine_data_df = pd.DataFrame(machine_data)

    engine = create_engine(f"mysql+mysqlconnector://{db_user}:{db_password}@localhost/PokeData")

    machine_data_df.to_sql('machine_moves', con=engine, if_exists='append', index=False)

    print("Data Inserted")

if __name__ == "__main__":
    insert_into_machine_table()
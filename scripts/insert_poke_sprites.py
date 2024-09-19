from db_connector import *

import pandas as pd
import requests
import sqlite3 
from sqlalchemy import create_engine
from datetime import datetime
import json

def get_sprite(x):
        while True:
            api_url = f"https://pokeapi.co/api/v2/pokemon/{x}"
            response = requests.get(api_url)
            if response.status_code != 200:
                print("Pokemon is not valid")
                return None
            elif response.status_code == 200:
                data = response.json()
                break

        return data

def collect_sprites():
    sprite_counter = 1

    sprite_list = {"poke_name": [], "front_sprite":[] , "front_shiny_sprite":[]}


    while True:
        
        sprites = get_sprite(sprite_counter)

        if not sprites:
            break

        #Get poke name for sprite
        poke_name = sprites['name']

        #Get regular and shiny sprite for pokemon entry
        front_sprite = sprites['sprites']['front_default']
        front_shiny_sprite = sprites['sprites']['front_shiny']

        #Append those entries to the sprite list
        sprite_list['poke_name'].append(poke_name)
        sprite_list['front_sprite'].append(front_sprite)
        sprite_list['front_shiny_sprite'].append(front_shiny_sprite)

        sprite_counter += 1

        #Prints every 50 pokemon passed to reduce text printed
        if sprite_counter % 50 == 0:
            print(poke_name, 'has been appended')
    
    return sprite_list

def create_sprite_table():
     
     mydb = db_connection()
    
     mycursor = mydb.cursor()

     mycursor.execute(""" 

        CREATE TABLE IF NOT EXISTS pokemon_sprites(
            poke_name varchar(50),
            front_sprite text,
            front_shiny_sprite text,

            PRIMARY KEY (poke_name)          
        );
    """)

def insert_sprites_into_db():

    create_sprite_table()

    sprite_data = collect_sprites()

    sprite_df = pd.DataFrame(sprite_data, index= None)

    engine = create_engine(f"mysql+mysqlconnector://{db_user}:{db_password}@localhost/PokeData")

    sprite_df.to_sql('pokemon_sprites', con=engine, if_exists='append', index=False)

    print("Data Inserted")

if __name__ == "__main__":
    insert_sprites_into_db()
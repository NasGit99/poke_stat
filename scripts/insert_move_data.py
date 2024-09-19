from db_connector import *
#Will move imports to a different file to reduce repetitiveness
import pandas as pd
import requests
import sqlite3 
from sqlalchemy import create_engine
from datetime import datetime
import json

def get_move(x):
        while True:
            api_url = f"https://pokeapi.co/api/v2/move/{x}"
            response = requests.get(api_url)
            if response.status_code != 200:
                print("Move is not valid")
                return None
            elif response.status_code == 200:
                data = response.json()
                break

        return data
    
def get_pokemon_move(x):
    while True:
            api_url = f"https://pokeapi.co/api/v2/pokemon/{x}"
            response = requests.get(api_url)
            if response.status_code != 200:
                print("Move is not valid")
                return None
            elif response.status_code == 200:
                data = response.json()
                break

    return data
     
def find_move_data():  
    #Importing all move data

    move_counter = 1

    move_data ={
        "id":[],
        "move_name":[],
        "move_type":[],
        "move_attack_type":[],
        "move_description":[],
        "attack":[],
        "pp":[],
        "priority":[],
        "stat_changed":[],
        "stat_changed_value":[]
           }

    while True:
        try: 
            selected_move = get_move(move_counter)
        
            move_id = selected_move['id']
            move_name = selected_move['name']
            move_type = selected_move['type']['name']
            move_attack_type = selected_move['damage_class']['name']
            
            try:
                move_description = selected_move['effect_entries'][0]['short_effect']
            except:
                move_description = 'n/a'
            move_attack = selected_move['power']
            move_pp = selected_move['pp']
            move_priority = selected_move['priority']
            #Below 2 need an if statement
            try:
                if selected_move['stat_changes'][0]['stat']['name'] is None:
                    move_stat_changed ='n/a'
                else:
                    move_stat_changed = selected_move['stat_changes'][0]['stat']['name']
                if selected_move['stat_changes'][0]['change'] is None:
                    move_stat_changed_value ='n/a'
                else:
                    move_stat_changed_value = selected_move['stat_changes'][0]['change']
            except:
                move_stat_changed = 'n/a'
                move_stat_changed_value = 'n/a'

        
        

            #Append values to dictionary
            if move_name not in move_data['move_name']:
                move_data['id'].append(move_id)
                move_data['move_name'].append(move_name)
                move_data['move_type'].append(move_type)
                move_data['move_attack_type'].append(move_attack_type)
                move_data['move_description'].append(move_description)
                move_data['attack'].append(move_attack)
                move_data['pp'].append(move_pp)
                move_data['priority'].append(move_priority)
                move_data['stat_changed'].append(move_stat_changed)
                move_data['stat_changed_value'].append(move_stat_changed_value)
            
            if move_id % 50 == 0:
                print(move_name, 'is appended')

            move_counter += 1
        


        except Exception as e:
        # If any error occurs, print the error and break the loop
            print(f"Error processing move: {e}")
            break
    return move_data

            

def find_pokemon_moveset_data():
    pokemon_move_counter = 1
    id_counter = 1

    pokemon_move_data ={
        "move_entry_id":[],
        "pokemon":[],
        "pokemon_id":[],
        "move_name":[],
        "level_learned_at":[],
        "learn_method":[],
        "game_name":[]
                    }


    while True:
        try:
            selected_pokemon = get_pokemon_move(pokemon_move_counter)
            pokemon_name = selected_pokemon['name']

            
            for index, move in enumerate(selected_pokemon['moves']):
                move_name = move['move']['name']  # Get the move name
                version_details = move['version_group_details']  # All version details for this move

                # Looping through each game version
                for game in version_details:
                    game_name = game['version_group']['name']  # Get the game name
                    level_learned_at = game['level_learned_at']  # Get the level learned in that game
                    learn_method = game['move_learn_method']['name']

                    # Append move data for each game to dictionary
                    pokemon_move_data['move_entry_id'].append(id_counter)
                    pokemon_move_data['pokemon'].append(pokemon_name)
                    pokemon_move_data['pokemon_id'].append(pokemon_move_counter)
                    pokemon_move_data['move_name'].append(move_name)
                    pokemon_move_data['level_learned_at'].append(level_learned_at)
                    pokemon_move_data['learn_method'].append(learn_method)
                    pokemon_move_data['game_name'].append(game_name)

                    id_counter +=1
            if pokemon_move_counter % 50 == 0:        
                print(pokemon_name, 'is appended')
                
            pokemon_move_counter +=1

        except Exception as e:
        # If any error occurs, print the error and break the loop
            print(f"Error processing move: {e}")
            break
    return pokemon_move_data       


def create_move_table():
     
     mydb = db_connection()
    
     mycursor = mydb.cursor()

     mycursor.execute(""" 

        CREATE TABLE IF NOT EXISTS pokemon_moves(
            id int,
            move_name text,
            move_type text,                                                     
            move_attack_type text,
            move_description text,
            attack int,
            pp int,
            priority int,
            stat_changed varchar(50),
            stat_changed_value varchar(50),

            PRIMARY KEY (id)          
        );
    """)
     
def create_pokemon_moveset_table():
     
     mydb = db_connection()
    
     mycursor = mydb.cursor()

     mycursor.execute(""" 
    CREATE TABLE IF NOT EXISTS pokemon_move_set(    
        move_entry_id int,
        pokemon varchar(100),
        pokemon_id int,
        move_name varchar(100),
        level_learned_at int,
        learn_method varchar(100),
        game_name varchar(100)          

    );
        """)

def insert_moves_data_into_db():

    create_move_table()


    move_list = find_move_data()

    move_df = pd.DataFrame(move_list, index= None)

    engine = create_engine(f"mysql+mysqlconnector://{db_user}:{db_password}@localhost/PokeData")

    move_df.to_sql('pokemon_moves', con=engine, if_exists='append', index=False)

    print("Data Inserted")

def insert_pokemon_moves_data_into_db():

    create_pokemon_moveset_table()

    pokemon_moveset = find_pokemon_moveset_data()

    pokemon_moveset_df = pd.DataFrame(pokemon_moveset, index= None)

    engine = create_engine(f"mysql+mysqlconnector://{db_user}:{db_password}@localhost/PokeData")

    pokemon_moveset_df.to_sql('pokemon_move_set', con=engine, if_exists='append', index=False)

    print("Data Inserted")

if __name__ == "__main__":
    insert_moves_data_into_db()
    insert_pokemon_moves_data_into_db()

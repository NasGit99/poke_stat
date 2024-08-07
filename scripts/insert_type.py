from db_connector import *

import pandas as pd
import requests
import sqlite3 
from sqlalchemy import create_engine
from datetime import datetime
import json

def get_types(x):
        while True:
            api_url = f"https://pokeapi.co/api/v2/type/{x}"
            response = requests.get(api_url)
            if response.status_code != 200:
                print("Type is not valid")
                return None
            elif response.status_code == 200:
                data = response.json()
                break

        return data

type_chart = {
    "ID": [] ,
    "Type_Name" :[],
    "Normal": [],
    "Fire": [],
    "Water": [],
    "Electric": [],
    "Grass": [],
    "Ice": [],
    "Fighting": [],
    "Poison": [],
    "Ground": [],
    "Flying": [],
    "Psychic": [],
    "Bug": [],
    "Rock": [],
    "Ghost": [],
    "Dragon": [],
    "Dark": [],
    "Steel": [],
    "Fairy": [],
    "Stellar":[]
}

def create_type_chart():
    import logging

    type_count = 1
    while True:
        try:
            type_data = get_types(type_count)
            if not type_data:
                break
        except Exception as e:
            logging.error(f"Could not insert {type_data} due to {e}")
        

        type_name = type_data['name'].capitalize()
        if type_name not in type_chart['Type_Name']:
            type_chart['Type_Name'].append(type_name)

        # Track processed types
        processed_types = set()

        type_chart['ID'].append(type_count)

        #Go through each weakness and append value. Value of 1 appended for all others
        for type_key in type_chart.keys():
            if type_key not in ["ID", "Type_Name"]:
                type_chart[type_key].append("1")

        # Process double damage
        for damage_type in type_data['damage_relations']['double_damage_from']:
            key = damage_type['name'].capitalize()
            if key in type_chart:
                type_chart[key][-1] = "2"

        # Process half damage
        for damage_type in type_data['damage_relations']['half_damage_from']:
            key = damage_type['name'].capitalize()
            if key in type_chart:
                type_chart[key][-1] = ".5"

        # Process no damage
        for damage_type in type_data['damage_relations']['no_damage_from']:
            key = damage_type['name'].capitalize()
            if key in type_chart:
                type_chart[key][-1] = "0"

        # for type_key in type_chart.keys():
        #     if type_key not in ["ID", "Type_Name"]:
        #         if len(type_chart[type_key]) < type_count:
        #             type_chart[type_key].append("1")

        processed_types.clear()
        type_count += 1

    poke_types = type_chart
    poke_types_df = type_df = pd.DataFrame(poke_types, columns = type_chart, index= None)

    return poke_types_df


def create_type_table():
     mydb = db_connection()
    
     mycursor = mydb.cursor()

     mycursor.execute("""    
    CREATE TABLE IF NOT EXISTS type_weakness(
        ID int,
        Type_Name varchar(25),
        Normal int,
        Fire  int,
        Water  int,
        Electric int, 
        Grass  int,
        Ice  int,
        Fighting  int,
        Poison  int,
        Ground  int,
        Flying  int,
        Psychic  int,
        Bug  int,
        Rock  int,
        Ghost  int,
        Dragon  int,
        Dark  int,
        Steel  int,
        Fairy  int,
        Stellar int
        
        PRIMARY KEY(id)
        ); 
    """)

def insert_type_weakness_into_table():

    type_chart_df = create_type_chart()

    engine = create_engine(f"mysql+mysqlconnector://{db_user}:{db_password}@localhost/PokeData")

    # Step 3: Convert the Pandas DataFrame to a format for MySQL table insertion
    type_chart_df.to_sql('type_weakness', con=engine, if_exists='append', index=False)

    print("Data Inserted")

insert_type_weakness_into_table()



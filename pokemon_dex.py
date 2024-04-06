import pandas as pd
import numpy as np
from pokemon_stat import *
import sqlite3 
from sqlalchemy import create_engine

#Goal is to import all pokemon data and write it to a database
#Future iterations will allow you to select 6 pokemon and randomize the moves for them.

def get_pokedex():
        while True:
            api_url = f"https://pokeapi.co/api/v2/pokemon/?limit=100000&offset=0"
            response = requests.get(api_url)
            if response.status_code != 200:
                print("Pokemon is not valid")
            elif response.status_code == 200:
                data = response.json()
                break

        return data
        

def sort_through_dex(x):
        while True:
                api_url = f"https://pokeapi.co/api/v2/pokemon/{x}"
                response = requests.get(api_url)
                if response.status_code != 200:
                    print("Pokemon is not valid")
                elif response.status_code == 200:
                    data = response.json()
                    break

        return data

#Use this to grab each pokemon name and run it through the api to get the information

def insert_into_dex():
    
    poke_list = []
    poke_names = (get_pokedex()['results'])

    #Comment this out below and insert a name into the poke_list to test
    for index, x in enumerate(poke_names):
        poke_list.append((x['name']))
    
    national_dex ={"poke_name":[],"type":[],"ability":[],"ability2":[],"hp":[],"attack":[],"defense":[],"spatk":[],"spdef":[],"spd":[]}

    for x in poke_list:

        value = sort_through_dex(x)
      
        national_dex["poke_name"].append(value['species']['name'])
        national_dex["type"].append(value['types'][0]['type']['name'])
        national_dex["ability"].append(value['abilities'][0]['ability']['name'])

        try:
            national_dex["ability2"].append(value['abilities'][1]['ability']['name'])
        except IndexError:
               national_dex["ability2"].append(None)

        national_dex["hp"].append(value['stats'][0]['base_stat'])
        national_dex["attack"].append(value['stats'][1]['base_stat'])
        national_dex["defense"].append(value['stats'][2]['base_stat'])
        national_dex["spatk"].append(value['stats'][3]['base_stat'])
        national_dex["spdef"].append(value['stats'][4]['base_stat'])
        national_dex["spd"].append(value['stats'][5]['base_stat'])

        print(f"{x} Inserted")

    dex_dataframe = pd.DataFrame(national_dex)
    dex_dataframe.to_sql("pokemon",con=engine, if_exists='append')

connection = sqlite3.connect('POKEDATA.db')
engine = create_engine("sqlite:///POKEDATA.db", echo = False)

# file = "POKEDATA"
# try: 
#   conn = sqlite3.connect(file) 
#   print("Database formed.") 
# except: 
#   print("Database not formed.")



if __name__ == "__main__":     
    insert_into_dex()
import uuid
import pandas as pd
import numpy as np
import requests
import sqlite3 
from sqlalchemy import create_engine
from datetime import datetime
import json




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
    import time
    import logging

    poke_list = []
    poke_names = (get_pokedex()['results'])

    #Comment this out below and insert a name into the poke_list to test
    for index, x in enumerate(poke_names):
        poke_list.append((x['name']))
    
    national_dex ={"id":[],"poke_name":[],"type":[], "type_2": [], "ability":[],"ability_2":[],"hp":[],"attack":[],"defense":[],"spatk":[],"spdef":[],"speed":[]}
    curr_time = time.time()

    # while True:
    #     if time.time() > curr_time + 60: #1 minute
    #         break
    #     try:

    i = 1

    for x in poke_list:

        value = sort_through_dex(x)

        national_dex['id'].append(i)
        national_dex["poke_name"].append(value['forms'][0]['name'])
        national_dex["type"].append(value['types'][0]['type']['name'])

        try:
            national_dex["type_2"].append(value['types'][1]['type']['name'])
        except:
            national_dex["type_2"].append(None)

        national_dex["ability"].append(value['abilities'][0]['ability']['name'])

        try:
            national_dex["ability_2"].append(value['abilities'][1]['ability']['name'])
        except IndexError:
            national_dex["ability_2"].append(None)

        national_dex["hp"].append(value['stats'][0]['base_stat'])
        national_dex["attack"].append(value['stats'][1]['base_stat'])
        national_dex["defense"].append(value['stats'][2]['base_stat'])
        national_dex["spatk"].append(value['stats'][3]['base_stat'])
        national_dex["spdef"].append(value['stats'][4]['base_stat'])
        national_dex["speed"].append(value['stats'][5]['base_stat'])

        print(f"{x} Inserted")

        i += 1

    return national_dex

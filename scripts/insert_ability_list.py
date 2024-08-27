import requests
import pandas as pd
from db_connector import *
from sqlalchemy import create_engine


def get_ability(x):
        while True:
            api_url = f"https://pokeapi.co/api/v2/ability/{x}"
            response = requests.get(api_url)
            if response.status_code != 200:
                print("Ability is not valid")
                return None
            elif response.status_code == 200:
                data = response.json()
                break

        return data

game_list = ['id','ability_name']
game_dict ={}


def insert_game_list():
    ability_counter = 1
    ability = get_ability(ability_counter)
    
    if ability:
        processed_games = set() 

        for ability_num in ability['flavor_text_entries']:
            game_name = ability_num['version_group']['name']

            if game_name not in processed_games:
                processed_games.add(game_name)
                if game_name not in game_list:
                    game_list.append(game_name.replace("-", "_"))


def insert_ability_list():
    
    ability_counter = 1

    try:
        ability = get_ability(ability_counter)
    except Exception as e:
        print(f"Ability not valid: {e}")
        
    while ability:  
        #Assign a value of N/A for each value as a default
        
        for type_key in game_dict.keys():
                    game_dict[type_key].append("n/a") 
                
        #Append ability name 
        
        ablity_name =  ability['name']
        game_dict['id'][-1]=(ability_counter)
        game_dict['ability_name'][-1]=(ablity_name)
        
        try:
            for ability_num in ability['flavor_text_entries']:
                
                #Checks to see if the ability is english and if the game name is in the game_list
                game = ability_num['version_group']['name'].replace("-","_")
                if ability_num['language']['name'] == 'en' and game in game_list:          
                    for type_key in game_dict.keys():
                        if type_key == game:
                    #Assign ability per games in the list to game_dict for last index value
                            game_dict[type_key][-1]=(ability_num['flavor_text'])
            print(f"{ablity_name}, has been appended")
        except Exception as e:
            print(e)
        ability_counter += 1
        try:
            ability = get_ability(ability_counter)
        except Exception as e:
            print(f"Ability not valid: {e}")
            break

def create_ability_table():
     mydb = db_connection()
    
     mycursor = mydb.cursor()

     mycursor.execute("""    
    CREATE TABLE IF NOT EXISTS abilities(
        id int,
        ability_name varchar(50),
        ruby_sapphire TEXT,
        emerald TEXT,
        firered_leafgreen TEXT,
        diamond_pearl TEXT,
        platinum TEXT,
        heartgold_soulsilver TEXT,
        black_white TEXT,
        black_2_white_2 TEXT,
        x_y TEXT,
        omega_ruby_alpha_sapphire TEXT,
        sun_moon TEXT,
        ultra_sun_ultra_moon TEXT,
        lets_go_pikachu_lets_go_eevee TEXT,
        sword_shield TEXT,
        scarlet_violet TEXT,
        PRIMARY KEY(id)
        ); 
    """)

def insert_abilities_into_table():

    ability_df = pd.DataFrame(game_dict)

    engine = create_engine(f"mysql+mysqlconnector://{db_user}:{db_password}@localhost/PokeData")

    # Step 3: Convert the Pandas DataFrame to a format for MySQL table insertion
    ability_df.to_sql('abilities', con=engine, if_exists='append', index=False)

    print("Data Inserted")

insert_game_list()
for game in game_list:
            game_dict = {key: [] for key in game_list}
insert_ability_list()
insert_abilities_into_table()
        
        


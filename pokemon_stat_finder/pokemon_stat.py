import requests

class Pokemon:
    #Get user input for pokemon request
    def get_pokemon():
        while True:
            poke_request= input("Type the 1st pokemon you want to look for:").lower()
            api_url = f"https://pokeapi.co/api/v2/pokemon/{poke_request}"
            response = requests.get(api_url)
            if response.status_code != 200:
                print("Pokemon is not valid")
            elif response.status_code == 200:
                data = response.json()
                break

        return data
        

    def get_pokemon_2():
        while True:
            poke_request_2= input("Type the 2nd pokemon you want to look for:").lower()
            api_url_2 = f"https://pokeapi.co/api/v2/pokemon/{poke_request_2}"
            response_2 = requests.get(api_url_2)
            if response_2.status_code != 200:
                print("Pokemon is not valid")
            elif response_2.status_code == 200:
                data_2 = response_2.json()
                break

        return data_2

    #initalize pokemon object
    def __init__ (self,name,types,abilities,hp,attack,defense,spatk,spdef,spd):
        self.name = name
        self.type = types
        self.abilities = abilities
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.spatk =spatk
        self.spdef = spdef
        self.spd = spd

      
    def define_defense():
        base_defense1 =(Pokemon1.defense + Pokemon1.spdef)
        base_defense2 =(Pokemon2.defense + Pokemon2.spdef)

        #List stats for Reference
    def list_stats ():
        print(f"Pokemon 1's Name is: {Pokemon1.name.capitalize()}")
        print(f"Pokemon 1's Type is: {Pokemon1.type.capitalize()}")
        print(f"Pokemon 1's Ability is: {Pokemon1.abilities.capitalize()}")
        print(f"Pokemon 1's HP is: {Pokemon1.hp}")
        print(f"Pokemon 1's Attack is: {Pokemon1.attack}")
        print(f"Pokemon 1's Defense is: {Pokemon1.defense}")
        print(f"Pokemon 1's Special Attack is: {Pokemon1.spatk}")
        print(f"Pokemon 1's Special Defense is: {Pokemon1.spdef}")
        print(f"Pokemon 1's Speed is: {Pokemon1.spd}")

        print(f"\nPokemon 2's Name is: {Pokemon2.name.capitalize()}")
        print(f"Pokemon 2's Type is: {Pokemon2.type.capitalize()}")
        print(f"Pokemon 2's Ability is: {Pokemon2.abilities.capitalize()}")
        print(f"Pokemon 2's HP is: {Pokemon2.hp}")
        print(f"Pokemon 2's Attack is: {Pokemon2.attack}")
        print(f"Pokemon 2's Defense is: {Pokemon2.defense}")
        print(f"Pokemon 2's Special Attack is: {Pokemon2.spatk}")
        print(f"Pokemon 2's Special Defense is: {Pokemon2.spdef}")
        print(f"Pokemon 2's Speed is: {Pokemon2.spd}")
        





if __name__ == "__main__":
    # Create two Pokémon
    poke_name = Pokemon.get_pokemon()
    poke_name2 =  Pokemon.get_pokemon_2()

    Pokemon1 = Pokemon(poke_name['species']['name'], poke_name['types'][0]['type']['name'],poke_name['abilities'][0]['ability']['name'],
    poke_name['stats'][0]['base_stat'],poke_name['stats'][1]['base_stat'],poke_name['stats'][2]['base_stat'],
    poke_name['stats'][3]['base_stat'],poke_name['stats'][4]['base_stat'],poke_name['stats'][5]['base_stat'])

    Pokemon2 = Pokemon(poke_name2['species']['name'],poke_name2['types'][0]['type']['name'],poke_name2['abilities'][0]['ability']['name'],
    poke_name2['stats'][0]['base_stat'],poke_name2['stats'][1]['base_stat'],poke_name2['stats'][2]['base_stat'],
    poke_name2['stats'][3]['base_stat'],poke_name2['stats'][4]['base_stat'],poke_name2['stats'][5]['base_stat'])

Pokemon.list_stats()    
# Start the battle


















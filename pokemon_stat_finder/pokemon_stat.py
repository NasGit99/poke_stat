import requests

class Pokemon:
    #Get user input for pokemon request
    def get_pokemon(poke_request):
        poke_request= input("Type the 1st pokemon you want to look for:").lower()
        api_url = f"https://pokeapi.co/api/v2/pokemon/{poke_request}"
        response = requests.get(api_url)
        if response.status_code() != '200':
            print("Pokemon is not valid")
        elif response.status_code() == '200':
            data = response.json()

        poke_request2= input("Type the 2nd pokemon you want to look for:").lower()
        api_url_2 = f"https://pokeapi.co/api/v2/pokemon/{poke_request2}"
        response_2 = requests.get(api_url_2)
        data_2 = response_2.json()

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

        #Define attack strength for Poke 1 & 2
    def define_attack_strength():

        base_attack1 = (Pokemon1.attack + Pokemon1.spatk)
        base_attack2 = (Pokemon2.attack + Pokemon2.spatk)
        # if base_attack1 > base_attack2: 
        #     print(f"{Pokemon1.name} is stronger")
        # else:
        #     print(f"{Pokemon2.name} is stronger")
    
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
        

    

Pokemon1 = Pokemon(Pokemon.data['species']['name'], Pokemon.data['types'][0]['type']['name'],Pokemon.data['abilities'][0]['ability']['name'],
Pokemon.data['stats'][0]['base_stat'],Pokemon.data['stats'][1]['base_stat'],Pokemon.data['stats'][2]['base_stat'],
Pokemon.data['stats'][3]['base_stat'],Pokemon.data['stats'][4]['base_stat'],Pokemon.data['stats'][5]['base_stat'])

Pokemon2 =Pokemon(Pokemon.data_2['species']['name'], Pokemon.data_2['types'][0]['type']['name'],Pokemon.data_2['abilities'][0]['ability']['name'],
Pokemon.data_2['stats'][0]['base_stat'],Pokemon.data_2['stats'][1]['base_stat'],Pokemon.data_2['stats'][2]['base_stat'],
Pokemon.data_2['stats'][3]['base_stat'],Pokemon.data_2['stats'][4]['base_stat'],Pokemon.data_2['stats'][5]['base_stat'])


Pokemon.get_pokemon


















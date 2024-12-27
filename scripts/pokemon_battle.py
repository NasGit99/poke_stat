import requests

class Pokemon:
    #Get user input for pokemon request
    def get_pokemon(count):
        while True:
            poke_request= input(f"Pokemon Selection # {count}:").lower()
            api_url = f"https://pokeapi.co/api/v2/pokemon/{poke_request}"
            response = requests.get(api_url)
            if response.status_code != 200:
                print("Pokemon is not valid")
            elif response.status_code == 200:
                data = response.json()
                break
        return data


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

        
    def battle_start ():

        while (Pokemon1.hp > 0) and (Pokemon2.hp > 0) :
            health_bar_1 = "=" * int(Pokemon1.hp/5)
            health_bar_2 = "=" * int(Pokemon2.hp/5)

            print(f"{Pokemon1.name.capitalize()} Health Bar: {health_bar_1}\n"
                    f"current health is {Pokemon1.hp}\n")
            
            print(f"{Pokemon2.name.capitalize()} Health Bar: {health_bar_2}\n"
                    f"current health is {Pokemon2.hp}\n")
            
            if Pokemon1.spd > Pokemon2.spd:

                print("Pokemon 1 attacks: \n")

                while True:

                    choice = input(f"{Pokemon1.name.capitalize()}: Select the type of attack: 1 for physical-attk, 2 for special-attk: \n") 
                        
                    if choice == "1":
                        Pokemon2.hp -= Pokemon1.attack/5            
                        print(f"Health Bar: {health_bar_2}\n")
                        print(f"{Pokemon2.name.capitalize()} pokemon health is now: {Pokemon2.hp}")
                        break


                    elif choice == "2":
                        Pokemon2.hp -= Pokemon1.spatk/5 
                        print(f"Health Bar: {health_bar_2}\n")
                        print(f"{Pokemon2.name.capitalize()} health is: {Pokemon2.hp}\n") 
                        break
                    else:
                        print("Invalid input! Please type 1 or 2.")
                
                if Pokemon2.hp <= 0:
                    print(f"{Pokemon2.name.capitalize()} has fainted. {Pokemon1.name.capitalize()} wins!")
                    break

                    # Pokemon 2 attacks second

                while True:
                    print(f"{Pokemon2.name.capitalize()} attacks next!")
                    choice_2 = input(f"{Pokemon2.name.capitalize()}: Select the type of attack: 1 for physical-attk, 2 for special-attk: \n") 

                    if choice_2 == "1":
                        Pokemon1.hp -= Pokemon2.attack / 5
                        print(f"Health Bar: {health_bar_1}\n")
                        print(f"{Pokemon1.name.capitalize()}'s health is now: {Pokemon1.hp}")
                        break

                    elif choice_2 == "2":
                        Pokemon1.hp -= Pokemon2.spatk / 5
                        print(f"Health Bar: {health_bar_1}\n")
                        print(f"{Pokemon1.name.capitalize()}'s health is now: {Pokemon1.hp}")
                        break
                    else:
                        print("Invalid input! Please type 1 or 2.")
                    
                if Pokemon1.hp <= 0:
                    print(f"{Pokemon1.name.capitalize()} has fainted. {Pokemon2.name.capitalize()} wins!")
                    break
                
            elif Pokemon2.spd > Pokemon1.spd:
                    # Pokemon 2 attacks first

                while True:
                    print(f"{Pokemon2.name.capitalize()} attacks first!")

                    choice_2 = input(f"{Pokemon2.name.capitalize()}: Select the type of attack: 1 for physical-attk, 2 for special-attk: \n") 

                    if choice_2 == "1":
                        Pokemon1.hp -= Pokemon2.attack / 5
                        print(f"Health Bar: {health_bar_1}\n")
                        print(f"{Pokemon1.name.capitalize()}'s health is now: {Pokemon1.hp}")
                        break

                    elif choice_2 == "2":
                        Pokemon1.hp -= Pokemon2.spatk / 5
                        print(f"Health Bar: {health_bar_1}\n")
                        print(f"{Pokemon1.name.capitalize()}'s health is now: {Pokemon1.hp}")
                        break

                    else:
                        print("Invalid input! Please type 1 or 2.")

                if Pokemon1.hp <= 0:
                    print(f"{Pokemon1.name.capitalize()} has fainted. {Pokemon2.name.capitalize()} wins!")
                    break

                    # Pokemon 1 attacks second
                while True:
                    print(f"{Pokemon1.name.capitalize()} attacks next!")

                    choice = input(f"{Pokemon1.name.capitalize()}: Select the type of attack: 1 for physical-attk, 2 for special-attk: \n") 

                    if choice == "1":
                        Pokemon2.hp -= Pokemon1.attack / 5
                        print(f"Health Bar: {health_bar_2}\n")
                        print(f"{Pokemon2.name.capitalize()}'s health is now: {Pokemon2.hp}")
                        break

                    elif choice == "2":
                        Pokemon2.hp -= Pokemon1.spatk / 5
                        print(f"Health Bar: {health_bar_2}\n")
                        print(f"{Pokemon2.name.capitalize()}'s health is now: {Pokemon2.hp}")
                        break

                    else:
                        print("Invalid input! Please type 1 or 2.")

                if Pokemon2.hp <= 0:
                    print(f"{Pokemon2.name.capitalize()} has fainted. {Pokemon1.name.capitalize().capitalize()} wins!")
                    break

def create_pokemon(pokemon_data):
        return Pokemon(
            pokemon_data['species']['name'],
            pokemon_data['types'][0]['type']['name'],
            pokemon_data['abilities'][0]['ability']['name'],
            pokemon_data['stats'][0]['base_stat'],
            pokemon_data['stats'][1]['base_stat'],
            pokemon_data['stats'][2]['base_stat'],
            pokemon_data['stats'][3]['base_stat'],
            pokemon_data['stats'][4]['base_stat'],
            pokemon_data['stats'][5]['base_stat']
    )

if __name__ == "__main__":

        # Create two Pokémon

        while True:
            count = 1

            poke_name = Pokemon.get_pokemon(count)

            count += 1
            
            poke_name2 =  Pokemon.get_pokemon(count)

            Pokemon1 = create_pokemon(poke_name)
            Pokemon2 = create_pokemon(poke_name2)

            Pokemon.list_stats()  

            user_input = 0
            while user_input != "1" and user_input != "2" and user_input != 3:
                user_input = input("\nWould you like to try again? Type 1 to restart, 2 to start the battle, or 3 to exit \n ")

                if user_input == "1":
                    print("\nRestarting the Pokémon creation...\n") 
                     
                elif user_input == "2":  
                    Pokemon.battle_start()
                    exit()

                elif user_input == "3":
                    print("Closing now")
                    exit()
                else:
                    print("\nInvalid input, please choose 1 or 2.\n")
                    
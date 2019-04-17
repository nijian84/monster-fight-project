from random import choice, randint
from common import load_file, input_yn, display_character_sheet, stat_mod
from terminaltables import AsciiTable
from inventory import display_inv
from combat import combat_menu, run, heal, attack_monster, attack_roll, defend

# Random encounter function
def random_encounter():
    """
    Randomly determines one of the monsters in the data.json, and returns dictionary containing monster data
    Args: none
    Returns: dictionary object
    """
    data = load_file("data.json")
    monster_block = choice(data["monsters"])
    return monster_block


# Display Monster block (as current form)
def display_monster(data):
    """
    Function that takes an dict of data, and displays it in a Table
    Args: data JSON
    Returns: nothing
    """
    monster_sheet = data
    monster_data = [
        ["Monster Name:", f'{monster_sheet["name"]}'],
        ["HP:", f'{monster_sheet["hp"]}'],
        ["Damage:", f'{monster_sheet["damage"]}'],
        ["Armor:", f'{monster_sheet["armor"]}'],
        ["Hit Bonus:", f'{monster_sheet["to_hit_bonus"]}'],
        ["XP Value:", f'{monster_sheet["xp"]}'],
    ]
    monster_table = AsciiTable(monster_data)
    print(monster_table.table)


# Function that takes in the monster block, turns it into 2 part array, containing separate stats
def full_encounter_block(monster_block):
    """
    Takes in dict, turns it into an array, and returns new data
    Args: monster_block DICT
    Returns: encounter_block DICT
    """
    encounter_block = []
    encounter_block.append(monster_block)
    encounter_block.append(
        {
            "current_hp": monster_block.get("hp"), 
            "initiative": randint(1, 20),
            "alive": True
        }
    )
    return encounter_block

# Function that displays Encounter menu, before combat
def encounter_menu():
    """
    Function that displays options, and returns choice
    Args: none
    Returns: user_choice STR
    """
    menu = [["Encounter Menu:"], ["Engage!"], ["Character"], ["Inventory"], ["Run!"], ["Quit"]]
    valid_list = ("engage", "run", "character", "inventory", "quit")
    menu_table = AsciiTable(menu)
    print(menu_table.table)
    while True:
        try:
            user_choice = input("Please enter your encounter choice:")
            user_choice = user_choice.lower()
        except ValueError:
            print("Please enter a valid encounter choice.")
            continue
        else:
            if user_choice in valid_list:
                return user_choice
            else:
                print("Please enter a valid encounter choice")


# Main funciont for handling Encounters
def main_encounter(char_details):
    """
    Function takes in char_details, from greeting function, and loops encounters
    Args: char_details JSON object
    Returns: nothing
    """
    print("")
    while True:
        user_input = input("Are you ready to proceed? Y/N ")
        user_input = input_yn(user_input)
        if user_input == "y":
            encounter = random_encounter()
            print("A wild.....")
            display_monster(encounter)
            print("appears!")
            print("")
            print("How would you like to proceed? ")
            choice = encounter_menu()
            if choice == "engage":
                main_combat(char_details, encounter)
            elif choice == "character":
                display_character_sheet(char_details)
            elif choice == "inventory":
                display_inv(char_details["uuid"])
            elif choice == "run":
                continue
            elif choice == "quit":
                break
        else:
            q_input = input("Do you want to quit? Y/N ")
            quit_input = input_yn(q_input)
            if quit_input == "y":
                break
            else:
                print("Ok, let's try again.")
                continue

# Main combat function loop
def main_combat(char_details, monster):
    monster_alive = True
    player_alive = True
    heal_used = False
    monster_block = full_encounter_block(monster)
    player_hp = char_details["hp"]
    print(monster_block)
    print(char_details)
    # Below is the Turn loop, player, then monster
    while monster_alive == True:
        # Player loop starts here:
        player_ac = char_details["armor"]
        user_choice = combat_menu()
        if user_choice == "attack":
            str_mod = stat_mod(char_details["stats"][0]["strength"])
            to_hit = attack_roll(str_mod, monster["armor"])
            if to_hit == True:
                print("hit monster")
            else:
                print("miss")
        elif user_choice == "defend":
            player_ac = defend(player_ac)
            print("AC increased by 2 for the turn.")
        elif user_choice == "heal":
            heal(player_hp, char_details["hp"], heal_used)
            continue
        elif user_choice == "run":
            if run(char_details["stats"][0]["dexterity"]):
                print("Ran successfully! Prepare for next encoutner.")
                break
            else:
                print("Failed to run! Oh no!")
                continue
        # Monster loop starts here:

        
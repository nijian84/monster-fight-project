from random import choice, randint
from common import load_file
from terminaltables import AsciiTable

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



# A common library of functions to be used in a little monster fighting game

from random import randint, choice
import uuid
import json
import os.path
import time
from terminaltables import AsciiTable


# Dice Rolling function
def roll_dice(sides):
    """
    Rolls 1 - sides
    Args: sides: int
    Return: int
    """
    return randint(1, sides)


# Character Creation suite:
# Pulls in the JSON file, and returns it as an object.
def load_file(filename):
    """
    Checks if JSON file exists, if not, creates it blank, otherwise loads JSON, and passes up as "data" variable
    Args: filename: str
    Returns: dictionary / json
    """
    if not os.path.exists("data.json"):
        data = {}
        with open("data.json", "w") as f:
            json.dump(data, f)
    else:
        with open("data.json") as f:
            json_data = json.loads(f.read())
    return json_data


# Function to grab modifier stat based on stat provided
def stat_mod(stat):
    """
    Function that takes in the stat and determines the bonus modifier and returns that
    Args: stat Int
    Returns stat_bonus Int
    """
    data = load_file("data.json")
    mods = data["stat_modifier"]
    stat_bonus = mods[f"{stat}"]
    return stat_bonus



# Function that takes item_id, iterates over all items in JSON Data file, and determines "type"
def check_item_type(item_id):
    """
    Load JSON file, takes item_id UUID, and iterates over weapons/armor to determine type and returns type
    Args: item_id STR
    Return: item_type STR
    """
    data = load_file("data.json")
    items = data["items"]

    for w in items["weapons"]:
        if item_id == w["item_id"]:
            item_type = "weapon"
            return item_type
    for a in items["armor"]:
        if item_id == a["item_id"]:
            item_type = "armor"
            return item_type


# Function for displaying a Character sheets
def display_character_sheet(character):
    """
    Function that displays a Character sheet, pulling in all character data and displaying it
    Args: character DICT
    Returns: nothing
    """
    character_sheet = character
    character_data = [
        ["Name:", f'{character_sheet["name"]}'],
        ["Level:", f'{character_sheet["level"]}'],
        ["Class:", f'{character_sheet["char_class"]}'],
        ["HP:", f'{character_sheet["hp"]}'],
        ["Damage:", f'{character_sheet["damage"]}'],
        ["Armor:", f'{character_sheet["armor"]}'],
        ["XP:", f'{character_sheet["xp"]}']
    ]
    stats = character_sheet["stats"][0]
    stats_data = [
        ["Stats:", "Values:"],
        ["Strength:", f'{stats["strength"]}'],
        ["Constitution:", f'{stats["constitution"]}'],
        ["Dexterity:", f'{stats["dexterity"]}'],
        ["Intelligence:", f'{stats["intelligence"]}'],
        ["Wisdom:", f'{stats["wisdom"]}'],
        ["Charisma:", f'{stats["charisma"]}']
    ]
    character_table = AsciiTable(character_data)
    stats_table = AsciiTable(stats_data)
    print(character_table.table)
    print("")
    print(stats_table.table)


# Input YN validator
def input_yn(user_input):
    """
    Function that takes in STR input, validates if it's Y or N answer, and prompts repeat if invalid response
    Args: user_input STR
    Returns: iser_input STR
    """
    yn_input = user_input.lower()
    while True:
        if yn_input.lower() in list("yn"):
            return yn_input
        else:
            yn_input = input("Please enter in a valid Y/N response: ")
            if yn_input.lower() in list("yn"):
                return yn_input
            else:
                continue

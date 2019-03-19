from common import roll_dice, load_file
from random import randint, choice
from kafka_func import kafka_produce
from db import check_character, get_id, write_character, fetch_char_details, write_items
import uuid
import json

# Function that accepts Input, and updates the JSON blob.
def create_character(data):
    """
    Function that takes in the json_file data, prompts for Character name
    Args: data: expected json data dictionary
    Returns: char_id STR, or character DICT
    """
    print("Welcome to Character creator!")
    char_name = str(input("Please enter Character name: "))
    if check_character(char_name):
        # Rewrite this logic
        print(f"Hello {char_name.capitalize()}, you already exist.")
        char_id = get_id(char_name)
        character = fetch_char_details(char_id)
        return character
    else:
        print(f"Welcome, {char_name}!")
        character = char_json_wrap(data, char_name)
        save_new_character(character)
        return character


# Takes JSON object, takes char name, wraps it all up into JSON, and returns JSON object
def char_json_wrap(data, char_name):
    """
    Takes in JSON data, char_name, and wraps it all up, and sends character JSON dict
    Args: data: json object, char_name: str
    Returns: data: json dict
    """
    char_id = str(uuid.uuid4())
    char_class = choose_class(data)
    class_stats = get_pref_class_stats(char_class, data["classes"])
    stats = roll_stats(class_stats)
    default_items = get_item_id(data, char_class)
    hp_bonus = con_bonus(data["stat_modifier"], stats)
    char_hp = get_hit_dice(char_class, data, hp_bonus)
    char_damage = get_char_dmg(default_items, data)
    char_ac = get_armor(default_items, data, stats)
    character = char_json(
        char_id, char_name, char_class, char_hp, char_damage, char_ac, stats
    )
    return character, default_items


# Validate class choice exists, and loop until valid, also prevent non str entrys
def choose_class(data):
    """
    Grabs class list data from JSON object, prompts user input, validates, and sets variable
    Args: data: json object
    Returns: char_class: str
    """
    # Map Class names to a variable
    class_list = [i["name"] for i in data["classes"]]
    print(f"Please choose a class from the list: {class_list}")
    while True:
        try:
            char_class = str(input("Please enter in Class name: "))
            char_class = char_class.lower()
        except ValueError:
            print("Please enter in a valid Class.")
            continue
        else:
            if char_class in class_list:
                print(f"You chose {char_class.capitalize()}.")
                return char_class
            else:
                print("Please enter a valid Class choice.")


# Pull ID's of default items based on class choice
def get_item_id(data, char_class):
    """
    Function that takes in JSON data, and char_class, and returns the UUID of the default items
    Args: data JSON, char_class STR
    Returns: default_weapon STR, default_armor STR
    """
    for _ in data["classes"]:
        if _["name"] == char_class:
            default_weapon = _["default_weapon"]
    for _ in data["classes"]:
        if _["name"] == char_class:
            default_armor = _["default_armor"]
    return {"default_weapon": default_weapon, "default_armor": default_armor}


# Iterate over all classes, and based on Class input, provide hit_dice
def get_hit_dice(char_class, data, hp_bonus):
    """
    Takes in char_class object, and determines hit dice, and returns HP value
    Args: char_class: str, data: json object, hp_bonus: int
    Returns: total_hp: int
    """
    for class_dice in data["classes"]:
        if class_dice["name"] == char_class:
            hit_dice = class_dice["hit_dice"]
    char_hp = roll_dice(hit_dice)
    hp_total = char_hp + hp_bonus
    print(f"Your HP is: {char_hp} + {hp_bonus} = {hp_total}")
    return hp_total


# Based on Stats Rolls, determines the constitution bonus for HP
def con_bonus(data, stats):
    """
    Takes in stat modifier data and stats rolls, and determines the modifier based on stats
    Args: data: list, stats: list
    Returns: bonus: int
    """
    con = stats["constitution"]
    bonus = data[f"{con}"]
    return bonus


# Provided list of default items, determines damage based on item ID
def get_char_dmg(default_items, data):
    """
    Takes in DICT of items, and JSON data, returns char_damage INT
    Args: default_items: DICT, data: json object
    Returns: char_damage: int
    """
    weapons = data["items"]["weapons"]
    for _ in weapons:
        if _["item_id"] == default_items["default_weapon"]:
            char_damage = _["damage_die"]
    print(f"Your weapon does d{char_damage} damage")
    return char_damage


# Provided list of default items, determines ac based on item ID
def get_armor(default_items, data, stats):
    """
    Takes in DICT of items, and JSON data, returns char_ac INT
    Args: default_items: DICT, data: json object
    Returns: char_ac: int
    """
    armor = data["items"]["armor"]
    for _ in armor:
        if _["item_id"] == default_items["default_armor"]:
            item_ac = _["ac"]
    bonus = data["stat_modifier"]
    dex = stats["dexterity"]
    ac_mod = bonus[f"{dex}"]
    char_ac = int(item_ac) + int(ac_mod)
    print(f"Your armor class is {char_ac}, base of {item_ac} with modifier of {ac_mod}")
    return char_ac


# Grabs list of stat preferences, and maps it to a list
def get_pref_class_stats(char_class, data):
    """
    Takes in char_class, and data, which contains all the class details
    Args: char_class: str, data: list of dicts
    Returns: class_stats: list of str
    """
    for _ in data:
        if _["name"] == char_class:
            class_stats = _["prefered_stats"]
            return class_stats
    class_stats = [
        "strength",
        "dexterity",
        "constitution",
        "intelligence",
        "wisdom",
        "charisma",
    ]
    return class_stats


# Appaned everything into the data JSON blob for saving purpose
def char_json(char_id, char_name, char_class, char_hp, char_damage, char_ac, stats):
    """
    Function to take in JSON data object, and all values, and returns an updated JSON dict
    Args: char_name: str, chas_class: str, char_hp: int, char_damage: int, char_ac: int
    Returns: json dict
    """
    return {
        "uuid": char_id,
        "name": char_name,
        "level": 1,
        "char_class": char_class,
        "hp": char_hp,
        "damage": char_damage,
        "armor": char_ac,
        "stats": [stats],
        "xp": 0,
    }


# Character creation function, which loads up the character, updates it, and then saves it.
def create():
    """
    Loads up file name, imports file into "json_file", updates character into json object, and writes it to file
    Args: None
    Output: None, writes to file
    """
    filename = "data.json"
    json_file = load_file(filename)
    char_data = create_character(json_file)
    return char_data


# Function to save character upon completion
def save_new_character(character):
    """
    Function that prompts user if they want to save character and items, if so, does to DB
    Args: character DICT
    Returns: nothing
    """
    char_data = character[0]
    char_items = character[1]
    response = str(input(f"Do you wish to Save {char_data['name']}? Y/N "))
    if response.lower() == "y":
        write_character(char_data)
        print("Character saved.")
        write_items(char_data["uuid"], char_items["default_weapon"])
        write_items(char_data["uuid"], char_items["default_armor"])
        print("Items saved")
        return
    else:
        print("Character not saved!")
        return


# Takes the list of stats, and maps them to their labels, and returns the dictionary
def map_stats(dice_set, class_stats):
    """
    Invoked in roll_stats, passed in the array of 6 ints, and maps them to the stat labels
    Args: dice_set: array of ints
    Returns: stat_map: dict of str+int
    """
    stat_map = {
        class_stats[0]: dice_set[0],
        class_stats[1]: dice_set[1],
        class_stats[2]: dice_set[2],
        class_stats[3]: dice_set[3],
        class_stats[4]: dice_set[4],
        class_stats[5]: dice_set[5],
    }
    return stat_map


# Specific function for rolling 3D6 dice, meant only for Stats
def _get_dice_roll():
    return randint(3, 18)


# Rolls up List of stats between 3-18, and returns this
def roll_stats(class_stats):
    """
    Rolls up set of stats, based on 3d6, or 3 to 18, invokes map_stats
    Args: none
    Returns: stats: dict
    """
    dice_set = [_get_dice_roll() for _ in range(6)]
    # Sort needs to be done in place, doesn't work when passed in function
    dice_set.sort(reverse=True)
    stats = map_stats(dice_set, class_stats)
    return stats

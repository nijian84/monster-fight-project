from db import fetch_char_inv
from common import load_file, check_item_type
from terminaltables import AsciiTable

# Function that displays an Existing characters inventory
def display_inv(char_id, inv_data=None):
    """
    Function that takes in Char_ID (default none), and gets dict of items from DB if needed
    Args: char_id STR = None, inv_data DICT = None
    Returns: nothing
    """
    data = load_file("data.json")
    items = data["items"]
    if inv_data == None:
        char_inv_list = fetch_char_inv(char_id)
    else:
        char_inv_list = inv_data

    inventory_data = []
    inventory_data.append(["Inventory", "Type"])
    for i in char_inv_list:
        for w in items["weapons"]:
            if i == w["item_id"]:
                item_type = check_item_type(w["item_id"])
                inventory_data.append([w["name"], f"{item_type}"])
        for a in items["armor"]:
            if i == a["item_id"]:
                item_type = check_item_type(a["item_id"])
                inventory_data.append([a["name"], f"{item_type}"])
    inventory = AsciiTable(inventory_data)
    print(inventory.table)


# Function that checks a character inventory for Weapons, and returns the ID
def get_weapon(char_id):
    """
    Function that takes UUID and fetchs only weapons from char inv list
    Args: char_id STR
    Returns: w STR (UUID)
    """
    char_inv_list = fetch_char_inv(char_id)
    for w in char_inv_list:
        is_weapon = check_item_type(w)
        if is_weapon == "weapon":
            return w

# Function for displaying a single item
def display_item(item_id):
    """
    Function that takes an item ID and displays it in a ASCII table
    Args: item_id (STR)
    Returns: nothing
    """
    data = load_file("data.json")
    items = data["items"]
    display = [["Item",""]]
    for w in items["weapons"]:
        if item_id == w["item_id"]:
            display.append(["Name: ", w["name"]])
            display.append(["Damage Dice: ", w["damage_die"]])
    for a in items["armor"]:
        if item_id == a["item_id"]:
            display.append(["Name: ", a["name"]])
            display.append(["AC Rating: ", a["ac"]])
    item_table = AsciiTable(display)
    print(item_table.table)

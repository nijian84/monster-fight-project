from db import fetch_char_inv
from common import load_file, check_item_type
from terminaltables import AsciiTable

# Function that displays an Existing characters inventory
def display_inv(char_name, char_id=None, inv_data=None):
    """
    Function that takes in Char_name, and Char_ID, and gets dict of items from DB if needed
    Args: Char_name STR, char_id STR = None, inv_data DICT = None
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

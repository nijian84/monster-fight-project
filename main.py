from common import display_character_sheet, check_item_type, load_file, input_yn
from character_creation import create
from db import fetch_char_details, get_id, create_tables, write_xp
from inventory import display_inv
from encounters import random_encounter, display_monster, full_encounter_block


# Initial greeting to create or load character data
def greeting():
    print("Welcome to Don's scrubby Monster Fighting!")
    user_input = str(input("Would you like to create a new Character? Y/N "))
    user_input = input_yn(user_input)
    if user_input == "y":
        char_details = create()
        display_character_sheet(char_details[0])
        display_inv(
            char_details[0]["name"], char_details[0]["uuid"], char_details[1].values()
        )
        return char_details
    else:
        secondary_input = str(
            input("Would you like to load an existing Character? Y/N ")
        )
        secondary_input = input_yn(secondary_input)
        if secondary_input == "y":
            char_name = str(input("Please enter your Character name: "))
            char_id = get_id(char_name)
            char_details = fetch_char_details(char_id)
            display_character_sheet(char_details)
            display_inv(char_name, char_id)
            return char_details
        elif secondary_input == "n":
            print("Ok. Quitting..")


if __name__ == "__main__":
    create_tables()
    character = greeting()
    
    
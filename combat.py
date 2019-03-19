from common import roll_dice
from terminaltables import AsciiTable


# Hit/Miss function
def to_hit_ac(ac, bonus, sides):
    """
    Takes AC and bonus, and determins if roll will be a hit or miss
    Args: ac, bonus
    Returns: boolean
    """
    hit_roll = roll_dice(sides)
    hit_result = hit_roll + bonus
    if hit_result >= ac:
        return True
    else:
        return False


# Function that displays the basic Combat menu
def combat_menu():
    menu = [
        ["Combat Menu:"],
        ["Attack"],
        ["Defend"],
        ["Run"]
    ]
    menu_table = AsciiTable(menu)
    print(menu_table.table)
    user_choice = input("Please enter your action choice:")
    



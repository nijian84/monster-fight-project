from common import roll_dice, stat_mod
from random import randint
from terminaltables import AsciiTable



# Function that displays the basic Combat menu
def combat_menu():
    """
    Function that displays table for Combat menu, and returns the users Choice
    Args: none
    Returns: user_choice STR
    """
    menu = [["Combat Menu:"], ["Attack"], ["Defend"], ["Heal"], ["Run"]]
    valid_list = ("attack", "defend", "heal", "run")
    menu_table = AsciiTable(menu)
    print(menu_table.table)
    while True:
        try:
            user_choice = input("Please enter your action choice:")
            user_choice = user_choice.lower()
        except ValueError:
            print("Please enter a valid Action choice.")
            continue
        else:
            if user_choice in valid_list:
                return user_choice
            else:
                print("Please enter a valid Action choice")


# Function that makes attack roll with modifier against enemy ac
def attack_roll(attack_mod, enemy_ac):
    """
    Function that takes attack_mod and enemy_ac and determines if a hit, and returns
    Args: attack_mod (int), enemy_ac (int)
    Returns: boolian
    """
    roll = randint(1, 20) + attack_mod
    if roll >= enemy_ac:
        return True
    else:
        return False


# Function that makes an attack on the monster, by taking in current_hp and damage, and determines remaining HP
def attack_monster(current_hp, damage):
    alive = True
    update_hp = current_hp - damage
    if update_hp <= 0:
        alive = False
        return update_hp, alive
    else:
        alive = True
        return update_hp, alive


# Function that gives ac bonus if chosing to defend
def defend(ac):
    """
    Function that takes in AC (int) and returns it at +2 value
    Args: ac (int)
    Returns: ac (int)
    """
    return ac + 2


# Function to perform heal action
def heal(current_hp, max_hp, heal_used):
    """
    Function that takes in a current HP, and max HP, and returns the updated current hp
    Args: current_hp (int), maxp_hp (int)
    Returns: current_hp (int), or nothing
    """
    if heal_used == False:
        if current_hp < max_hp:                
            print("Healed for 3 HP. This can only be done once per encounter.")
            current_hp = current_hp + 3
            if current_hp > max_hp:
                current_hp = max_hp
            heal_used = True
            return current_hp, heal_used
        else: 
            print("Player already at max HP. Heal not used.")
            return
    else:
        print("You can only heal once per encounter.")
        return


# Function that determines if you successfully run away
def run(dex_mod):
    """
    Funtion that determines if user runs away, checks random value against 10 + mod
    Args: dex_mod INT
    Returns: boolian
    """
    dc = 10
    mod = stat_mod(dex_mod)
    if (randint(1, 20) + mod) > dc:
        return True
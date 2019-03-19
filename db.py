import peewee
from playhouse.postgres_ext import JSONField
from playhouse.pool import PostgresqlExtDatabase
from common import check_item_type

# Connection information
db = PostgresqlExtDatabase(
    # First entry is DB name
    "testing",
    user="testing",
    host="10.203.0.75",
    password="testing",
    port="5432",
)

# Defined Schema, Meta data mapped to DB variable above
class Character(peewee.Model):
    uuid = peewee.UUIDField(primary_key=True, unique=True)
    name = peewee.CharField()
    level = peewee.IntegerField()
    char_class = peewee.CharField()
    hp = peewee.IntegerField()
    damage = peewee.IntegerField()
    armor = peewee.IntegerField()
    stats = JSONField()
    xp = peewee.IntegerField()

    class Meta:
        database = db


# Define Schema for Items mapping
class Character_Inventory(peewee.Model):
    char_uuid = peewee.UUIDField()
    item_id = peewee.UUIDField()
    item_type = peewee.CharField()

    class Meta:
        database = db


# Creates Tables for saving Characters
def create_tables():
    """
    Function for creating the necessary Table, with the correct Schema
    Args: none
    Returns: none
    """
    db.connect()
    db.create_tables([Character])
    db.create_tables([Character_Inventory])
    db.commit()
    db.close()


# Writes character data to Character table
def write_character(data):
    """
    Function to write Character to DB Table
    Args: data JSON Dict
    Returns: nothing
    """
    db.connect(reuse_if_open=True)
    Character.create(**data)
    db.commit()
    db.close()


# Write character Items and Character relations
def write_items(char_id, item_id):
    """
    Takes char_id, item_id and determines item type, and writes them all to Character_Item table
    Args: char_id STR, item_id STR
    returns: nothing
    """
    item_type = check_item_type(item_id)
    db.connect(reuse_if_open=True)
    Character_Inventory.create(char_uuid=char_id, item_id=item_id, item_type=item_type)
    db.commit()
    db.close

# Function to write XP rewards to specific character
def write_xp(char_id, xp_value):
    """
    Function that takes in char_id, an xp_value, and connects to DB, and writes the Xp value
    Args: char_id STR, xp_value INT
    Returns: nothing
    """
    db.connect(reuse_if_open=True)
    update = Character.update(xp = xp_value).where(Character.uuid == char_id)
    update.execute()
    db.close()


# Checks if Character name already exists
def check_character(char_name):
    """
    Function that queries DB table if Character name exists, and returns UUID if true
    Args: char_name STR
    Returns: query STR
    """
    db.connect(reuse_if_open=True)
    query = Character.select().where(Character.name ** char_name).exists()
    db.close()
    return query


# Fuction that fetches the character ID if exists
def get_id(char_name):
    """
    Function that uses Character name to fetch UUID
    Args: char_name STR
    Returns: query.uui
    """
    db.connect(reuse_if_open=True)
    query = Character.select(Character.uuid).where(Character.name ** char_name).get()
    return query.uuid


# Function to fetch the data of an Existing character
def fetch_char_details(char_uuid):
    """
    Function that takes UUID, queries DB, fetches all the data and returns it
    Args: char_uuid STR
    Returns: dict
    """
    query = Character.select().where(Character.uuid == char_uuid).get()
    return {
        "uuid": query.uuid,
        "name": query.name,
        "level": query.level,
        "char_class": query.char_class,
        "hp": query.hp,
        "damage": query.damage,
        "armor": query.armor,
        "stats": query.stats,
        "xp": query.xp,
    }


# Fetches inventory data from DB
def fetch_char_inv(character):
    """
    Connects to DB and returns Inventory data
    Args: Character STR
    Returns: DICT
    """
    query = Character_Inventory.select().where(
        Character_Inventory.char_uuid == character
    )
    return [str(item.item_id) for item in query]


# def update_inventory(char_id, item_id):
#     db.connect(reuse_if_open=True)

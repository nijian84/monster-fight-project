from random import choice


class Player(object):
    def __init__(self, name: str = ""):
        self.name = name if name else "Anonymous"
        self.level = 0

    def level_up(self):
        self.level += 1

    @classmethod
    def create(cls, name: str = ""):
        """Classmethods are factory methods that return an instantiated object."""
        return cls(name)

    @classmethod
    def create_monster(cls):
        monster = choice(['kobold', 'bear', 'troll'])
        return cls(monster)

    @staticmethod
    def greeting():
        """Functions that don't interact with encapsulated data, but may be related."""        
        print("Hello good sir.")


def get_monsters():
    return [
        {
            "name": "kobold",
            "hp": 5,
            "armor": 12,
            "damage": 4,
            "to_hit_bonus": 4,
            "xp": 25,
        },
        {
            "name": "bear",
            "hp": 34,
            "armor": 11,
            "damage": 8,
            "to_hit_bonus": 6,
            "xp": 200,
        },
    ]


if __name__ == "__main__":
    p1 = Player.create("Zeal")
    p1.level_up()
    print(f"My name is {p1.name}, my level is {p1.level}")

    Player.greeting()

    monsters = []
    for m in get_monsters():
        monsters.append(Player.create(name=m.get("name", "")))
    monsters = [m.name for m in monsters]
    print(monsters)

    more_monsters = [Player.create_monster() for i in range(1, 9)]
    for m in more_monsters:
        print(m.name)
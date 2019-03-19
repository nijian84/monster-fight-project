import json
from random import choice

# with open("data.json") as f:
#     #Read in the JSON file into "content" as a large String
#     content = f.read()
#     #Converts "content" into dictionary with appropriate values
#     data = json.loads(content)

#print(len(data['monsters']))

with open("data.json") as f:
        content = json.loads(f.read())

def random_encounter():
    monster_block = choice(content["monsters"])
    return monster_block


def get_yn():
        while True:
                char = input('Please enter something: ')
                if char.lower() in list('yn'):
                        return char
                print('Please dont screw up the input')

get_yn()

if (get_yn() == 'y'):
        y
else:
        n


print(random_encounter())
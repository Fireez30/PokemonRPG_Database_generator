from json.decoder import NaN
from shutil import move

from parsers import to_serializable
import pandas as pd
import json

from pokemon_data import FullMove, Ability

if __name__ == '__main__':
    """
    Index(['Attack Name', 'Type', 'Class', 'Frequency', 'Range', 'AC', 'DB',
       'Effect', 'Versatile Effect', 'Attack Tier'],
      dtype='str')
    """
    final_str = "Abilities : \n"
    with open("../data/final_abilities_ptu.json", "r") as f:
        abilities = json.load(f)
    for ability in abilities:
        if ability["effect"].strip() == "":
            final_str += ability["name"]+"\n"
    final_str += "\n"
    final_str += "Moves : \n"
    with open("../data/final_moves_ptu.json", "r") as f:
        moves = json.load(f)
    for move in moves:
        if move["effect"].strip() == "":
            final_str += move["name"]+"\n"
    final_str += "\n"

    f = open("empty_moves_abilities.txt","w+")
    f.write(final_str)
    f.close()
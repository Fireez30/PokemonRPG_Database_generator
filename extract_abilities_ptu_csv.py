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
    with open("data/final_abilities.json", "r") as f:
        db_pokemons = json.load(f)
    df = pd.read_csv('data/ptuabilities.csv',header=0)
    moves = []
    move_objs_array = []
    for index, row in df.iterrows():
        moves.append(Ability(row["Name"],row["Effect"],-1))

    for movedb in db_pokemons:
        existing_moves = [move for move in moves if move.name == movedb["name"]]
        if len(existing_moves) > 0:
            existing_moves[0].effect = (movedb["effect"] if existing_moves[0].effect == "" or existing_moves[0].effect is None or existing_moves[0].effect.lower() == "none" else existing_moves[0].effect)
            existing_moves[0].id = (movedb["id"] if "id" in movedb and existing_moves[0].id == -1 else existing_moves[0].id)
        else:
            moves.append(Ability(movedb["name"], movedb["effect"],(movedb["id"] if "id" in movedb else -1)))

    csv = "Name,Effect"
    for abili in moves:
        if abili is not None and abili != "":
            csv += "\n"+abili.name+",\""+abili.effect+"\""
    f = open("data/final_abilities_ptu.csv","w+")
    f.write(csv)
    f.close()

    with open("data/abilities.json", "w", encoding="utf-8") as f_json:
        json.dump(
            to_serializable(moves),
            f_json,
            indent=4,  # pretty print
            ensure_ascii=False
        )

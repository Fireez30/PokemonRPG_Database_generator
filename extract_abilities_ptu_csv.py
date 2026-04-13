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
    with open("output/redux/abilities.json", "r") as f:
        db_pokemons = json.load(f)
    df = pd.read_csv('data/ptuabilities.csv',header=0)
    moves = []
    move_objs_array = []

    for movedb in db_pokemons:
        moves.append(Ability(movedb["name"], movedb["effect"],(movedb["id"] if "id" in movedb else -1)))


    for index, row in df.iterrows():
        existing_moves = [move for move in moves if move.name == row["Name"]]
        if len(existing_moves) > 0:
            moves.append(Ability(row["Name"]+"_pte", row["Effect"], -1))
        else:
            moves.append(Ability(row["Name"], row["Effect"], -1))



    csv = "Name,Effect"
    for abili in moves:
        if abili is not None and abili != "":
            csv += "\n"+abili.name+",\""+abili.effect+"\""
    f = open("output/pte/abilities.csv","w+")
    f.write(csv)
    f.close()

    with open("output/pte/abilities.json", "w", encoding="utf-8") as f_json:
        json.dump(
            to_serializable(moves),
            f_json,
            indent=4,  # pretty print
            ensure_ascii=False
        )

    for abili in moves:
        if abili is not None and abili != "":
            csv += "\n"+abili.name+",\""+abili.effect+"\""
    f = open("output/finals/abilities.csv","w+")
    f.write(csv)
    f.close()

    with open("output/finals/abilities.json", "w", encoding="utf-8") as f_json:
        json.dump(
            to_serializable(moves),
            f_json,
            indent=4,  # pretty print
            ensure_ascii=False
        )

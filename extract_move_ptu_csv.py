from json.decoder import NaN
from shutil import move

from parsers import to_serializable
import pandas as pd
import json

from pokemon_data import FullMove,accepted_classes,accepted_ACs,accepted_freqs,accepted_types
def is_two_digit_number(s):
    return s.isdigit() and len(s) <= 2


if __name__ == '__main__':
    """
    Index(['Attack Name', 'Type', 'Class', 'Frequency', 'Range', 'AC', 'DB',
       'Effect', 'Versatile Effect', 'Attack Tier'],
      dtype='str')
    """
    with open("data/final_moves.json", "r") as f:
        db_pokemons = json.load(f)
    df = pd.read_csv('data/ptumoves.csv',header=0)
    moves = []
    move_objs_array = []
    rolls_by_db = {}
    for movedb in db_pokemons:
        if "damage_base" in movedb:
            if not movedb["damage_base"] in rolls_by_db or rolls_by_db[movedb["damage_base"]] is None or rolls_by_db[movedb["damage_base"]] == "":
                rolls_by_db[movedb["damage_base"]] = movedb["roll"]
    for index, row in df.iterrows():
        moves.append(FullMove(row["Attack Name"],row["Type"], row["Frequency"],(str(int(row["AC"])) if "AC" in row and row["AC"] is not None and str(row["AC"]).lower() != "nan" and row["AC"] != NaN else ""),str(int(row["DB"])) if "DB" in row and row["DB"] is not None and str(row["DB"]).lower() != "nan" and row["DB"] != NaN else "","",row["Class"],row["Range"],row["Effect"],"","","","",[]))
    for move in moves:
        if move.damage_base != "":
            if move.damage_base in rolls_by_db:
                move.roll = rolls_by_db[move.damage_base]
            else:
                print("error finding roll for damage base : "+str(move["damage_base"]))
                exit()
    for movedb in db_pokemons:
        existing_moves = [move for move in moves if move.move == movedb["move"]]
        if len(existing_moves) > 0:
            print("found move : " + existing_moves[0].move)
            movedb["frequency"] = movedb["frequency"].replace("At Will","At-Will").replace("Daily x2/em>","Daily x2").replace("Scence","Scene")
            movedb["classe"] = movedb["classe"].replace("STATUS","Status")
            existing_moves[0].frequency = existing_moves[0].frequency.replace("At Will","At-Will").replace("Daily x2/em>","Daily x2").replace("Scence","Scene")
            existing_moves[0].classe = existing_moves[0].classe.replace("STATUS","Status")
            if not is_two_digit_number(movedb["AC"]) and not movedb["AC"].strip() in accepted_ACs:
                movedb["AC"] = existing_moves[0].AC
                print("updated AC")
            if not movedb["frequency"] in accepted_freqs:
                movedb["frequency"] = existing_moves[0].frequency
                print("updated freq")
            if not movedb["type"] in accepted_types:
                movedb["type"] = existing_moves[0].type
                print("updated type")
            if not movedb["classe"] in accepted_classes:
                movedb["classe"] = existing_moves[0].classe
                print("updated classe")
            existing_moves[0].type = (movedb["type"] if existing_moves[0].type == "" or existing_moves[0].type is None or existing_moves[0].type.lower() == "none" else existing_moves[0].type)
            existing_moves[0].frequency = (movedb["frequency"] if existing_moves[0].frequency == "" or existing_moves[0].frequency is None or existing_moves[0].frequency.lower() == "none" else existing_moves[0].frequency)
            existing_moves[0].AC = (movedb["AC"] if existing_moves[0].AC == "" or existing_moves[0].AC is None or existing_moves[0].AC.lower() == "none" else existing_moves[0].AC)
            existing_moves[0].damage_base = (movedb["damage_base"] if existing_moves[0].damage_base == "" or existing_moves[0].damage_base is None or existing_moves[0].damage_base.lower() == "none" else existing_moves[0].damage_base)
            existing_moves[0].roll = (movedb["roll"] if existing_moves[0].roll == "" or existing_moves[0].roll is None or existing_moves[0].roll.lower() == "none" else existing_moves[0].roll)
            existing_moves[0].classe = (movedb["classe"] if existing_moves[0].classe == "" or existing_moves[0].classe is None or existing_moves[0].classe.lower() == "none" else existing_moves[0].classe)
            existing_moves[0].range = (movedb["range"] if existing_moves[0].range == "" or existing_moves[0].range is None or existing_moves[0].range.lower() == "none" else existing_moves[0].range)
            existing_moves[0].effect = (movedb["effect"] if existing_moves[0].effect == "" or existing_moves[0].effect is None or existing_moves[0].effect.lower() == "none" else existing_moves[0].effect)
            existing_moves[0].blessing = (movedb["blessing"] if existing_moves[0].blessing == "" or existing_moves[0].blessing is None or existing_moves[0].blessing.lower() == "none" else existing_moves[0].blessing)
            existing_moves[0].special_effect = (movedb["special_effect"] if existing_moves[0].special_effect == "" or existing_moves[0].special_effect is None or existing_moves[0].special_effect.lower() == "none" else existing_moves[0].special_effect)
            existing_moves[0].contest_type = (movedb["contest_type"] if existing_moves[0].contest_type == "" or existing_moves[0].contest_type is None or existing_moves[0].contest_type.lower() == "none" else existing_moves[0].contest_type)
            existing_moves[0].contest_effect = (movedb["contest_effect"] if existing_moves[0].contest_effect == "" or existing_moves[0].contest_effect is None or existing_moves[0].contest_effect.lower() == "none" else existing_moves[0].contest_effect)
            existing_moves[0].extra_lines = (movedb["extra_lines"] if existing_moves[0].extra_lines == [] else existing_moves[0].extra_lines)
            existing_moves[0].id = (movedb["id"] if "id" in movedb and existing_moves[0].id == -1 else existing_moves[0].id)


        else:
            moves.append(FullMove(movedb["move"], movedb["type"], movedb["frequency"], movedb["AC"],movedb["damage_base"], movedb["roll"], movedb["classe"],
                                  movedb["range"], movedb["effect"], movedb["blessing"] ,movedb["special_effect"], movedb["contest_type"], movedb["contest_effect"], movedb["extra_lines"],(movedb["id"] if "id" in movedb else -1)))

    csv = "Move,Freq,AC,Type,Roll,Dmg. Type,Range,Special Effect"
    for move in moves:
        csv += "\n"+move.to_csv()
    f = open("data/final_moves_ptu.csv","w+")
    f.write(csv)
    f.close()

    with open("data/final_moves_ptu.json", "w", encoding="utf-8") as f_json:
        json.dump(
            to_serializable(moves),
            f_json,
            indent=4,  # pretty print
            ensure_ascii=False
        )

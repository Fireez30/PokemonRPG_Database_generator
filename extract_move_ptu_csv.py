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
    with open("output/redux/moves.json", "r") as f:
        redux_moves = json.load(f)
    df = pd.read_csv('data/ptumoves.csv',header=0)
    pte_moves = []
    final_moves=[]
    move_objs_array = []
    rolls_by_db = {}
    for reduxmove in redux_moves:
        if "damage_base" in reduxmove:
            if not reduxmove["damage_base"] in rolls_by_db or rolls_by_db[reduxmove["damage_base"]] is None or rolls_by_db[reduxmove["damage_base"]] == "":
                rolls_by_db[reduxmove["damage_base"]] = reduxmove["roll"]
        final_moves.append(
            FullMove(reduxmove["move"], reduxmove["type"], reduxmove["frequency"], reduxmove["AC"], reduxmove["damage_base"],
                     reduxmove["roll"], reduxmove["classe"],
                     reduxmove["range"], reduxmove["effect"], reduxmove["blessing"], reduxmove["special_effect"],
                     reduxmove["contest_type"], reduxmove["contest_effect"], reduxmove["extra_lines"],
                     (reduxmove["id"] if "id" in reduxmove else -1)))

    for index, row in df.iterrows():
        pte_moves.append(FullMove(row["Attack Name"], row["Type"], row["Frequency"], (str(int(row["AC"])) if "AC" in row and row["AC"] is not None and str(row["AC"]).lower() != "nan" and row["AC"] != NaN else ""), str(int(row["DB"])) if "DB" in row and row["DB"] is not None and str(row["DB"]).lower() != "nan" and row["DB"] != NaN else "", "", row["Class"], row["Range"], row["Effect"], "", "", "", "", []))
        #final_moves.append(FullMove(row["Attack Name"],row["Type"], row["Frequency"],(str(int(row["AC"])) if "AC" in row and row["AC"] is not None and str(row["AC"]).lower() != "nan" and row["AC"] != NaN else ""),str(int(row["DB"])) if "DB" in row and row["DB"] is not None and str(row["DB"]).lower() != "nan" and row["DB"] != NaN else "","",row["Class"],row["Range"],row["Effect"],"","","","",[]))
    for move in pte_moves:
        if move.damage_base != "":
            if move.damage_base in rolls_by_db:
                move.roll = rolls_by_db[move.damage_base]
            else:
                print("error finding roll for damage base : "+str(move["damage_base"]))
                exit()
    for ptemove in pte_moves:
        existing_moves = [move for move in redux_moves if move["move"] == ptemove.move]
        if len(existing_moves) > 0:
            ptemove.move = ptemove.move + "_pte"
        ptemove.frequency = ptemove.frequency.replace("At Will", "At-Will").replace("Daily x2/em>", "Daily x2").replace("Scence", "Scene")
        ptemove.classe = ptemove.classe.replace("STATUS", "Status")
        final_moves.append(ptemove)

    csv = "Move,Freq,AC,Type,Roll,Dmg. Type,Range,Special Effect"
    for move in final_moves:
        csv += "\n"+move.to_csv()
    f = open("output/pte/moves.csv","w+")
    f.write(csv)
    f.close()

    with open("output/pte/moves.json", "w", encoding="utf-8") as f_json:
        json.dump(
            to_serializable(final_moves),
            f_json,
            indent=4,  # pretty print
            ensure_ascii=False
        )

    csv = "Move,Freq,AC,Type,Roll,Dmg. Type,Range,Special Effect"
    for move in final_moves:
        csv += "\n"+move.to_csv()
    f = open("output/finals/moves.csv","w+")
    f.write(csv)
    f.close()

    with open("output/finals/moves.json", "w", encoding="utf-8") as f_json:
        json.dump(
            to_serializable(final_moves),
            f_json,
            indent=4,  # pretty print
            ensure_ascii=False
        )
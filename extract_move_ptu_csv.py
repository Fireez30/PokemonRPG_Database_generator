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
            FullMove(
                name=reduxmove["name"],
                types=reduxmove["types"],
                frequency=reduxmove["frequency"],
                AC=reduxmove["AC"],
                damage_base=reduxmove["damage_base"],
                roll=reduxmove["roll"],
                m_class=reduxmove["m_class"],
                range=reduxmove["range"],
                effect=reduxmove["effect"],
                blessing=reduxmove.get("blessing"),
                special_effect=reduxmove.get("special_effect"),
                contest_types=reduxmove.get("contest_types"),
                contest_effect=reduxmove.get("contest_effect"),
                extra_lines=reduxmove.get("extra_lines", []),
                id=(reduxmove["id"] if "id" in reduxmove else -1)
            )
        )

    for index, row in df.iterrows():
        ac_val = str(int(row["AC"])) if "AC" in row and row["AC"] is not None and str(row["AC"]).lower() != "nan" and row["AC"] != NaN else ""
        db_val = int(row["DB"]) if "DB" in row and row["DB"] is not None and str(row["DB"]).lower() != "nan" and row["DB"] != NaN else -1
        type_val = str(row["Type"]).strip() if "Type" in row and row["Type"] else "Normal"
        pte_moves.append(FullMove(
            name=row["Attack Name"],
            types=[t.strip() for t in type_val.split("/") if t.strip()],
            frequency=str(row["Frequency"]).strip() if "Frequency" in row else "TBD",
            AC=ac_val,
            damage_base=db_val,
            roll="",
            m_class=str(row["Class"]).strip() if "Class" in row else "Status",
            range=str(row["Range"]).strip() if "Range" in row else "",
            effect=str(row["Effect"]).strip() if "Effect" in row else "",
            blessing=None,
            special_effect=None,
            contest_types=None,
            contest_effect=None,
            extra_lines=[]
        ))

    for ptemove in pte_moves:
        if ptemove.damage_base != -1:
            if ptemove.damage_base in rolls_by_db:
                ptemove.roll = rolls_by_db[ptemove.damage_base]
            else:
                print("error finding roll for damage base : "+str(ptemove.damage_base))
                exit()
    for ptemove in pte_moves:
        existing_moves = [m for m in redux_moves if m["name"] == ptemove.name]
        if len(existing_moves) > 0:
            ptemove.name = ptemove.name + "_pte"
        ptemove.frequency = ptemove.frequency.replace("At Will", "At-Will").replace("Daily x2/em>", "Daily x2").replace("Scence", "Scene")
        ptemove.m_class = ptemove.m_class.replace("STATUS", "Status")
        final_moves.append(ptemove)

    csv = "Move,Freq,AC,Type,Roll,Dmg. Type,Range,Special Effect"
    for m in final_moves:
        csv += "\n"+m.to_csv()
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
    for m in final_moves:
        csv += "\n"+m.to_csv()
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
